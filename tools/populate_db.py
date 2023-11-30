"""populates database"""

import os
import json
from thefuzz import fuzz as tfuzz  # string similarities
from rapidfuzz import process
import numpy as np
from tqdm import tqdm
from numba import njit
from datetime import datetime
import psycopg2
from uuid import uuid4
import pickle
import re
from sqlalchemy import create_engine
import pandas as pd
from getpass import getpass
from dtypes import Market, Product

#// from utils.ner import NERModel

# ==============================================================================
# FUNCTIONS AND CONSTANTS
# ==============================================================================

@njit(parallel=True)
def build_edge_list(matrix, thresh):
    fair_sz = max(1, len(matrix) ** 2 // 1000)  # assume each product has similarity > threshold for less then 0.1% of all products
    leftnodes = np.ones(fair_sz)
    rightnodes = np.ones(fair_sz)
    similarities = np.ones(fair_sz)
    k = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if j <= i:
                continue
            val = matrix[i][j]
            if val >= thresh:
                leftnodes[k] = i
                rightnodes[k] = j
                similarities[k] = val
                k += 1
                # if k > fair_sz:
                #     print(f"\033[91mk = {k}, increase fair-sz in build_edge_list(..)\033[0m")
                #     return
    return k, leftnodes, rightnodes, similarities


@njit
def pairs2refine(m, thresh=70):
    l = []
    for i in range(len(m)):
        for j, val in enumerate(m[i][i+1:]):
            if thresh <= val < 100:
                l.append((i,j))
    return l


def similarity(tags1, tags2):
    """geometric mean of set ratios"""
    combined_score = 1
    n_scores = 0
    for label in ["PRO", "MAR", "ESP", "TAM", "QUA"]:
        if label not in tags1 and label not in tags2:
            continue # ignore labels absent from both tag sets (uninformative)
        if label not in tags1 or label not in tags2:
            combined_score = 0 # TODO too consrevative? We are zeroing out the whole score if a tag appears in only one of the args
            n_scores += 1
        else:
            label_score = tfuzz.token_set_ratio(tags1[label], tags2[label])
            # label_score /= 100  # fuzz returns value in 0-100 range
            combined_score *= label_score
            n_scores += 1
    return np.array(combined_score ** (1 / n_scores), dtype=np.int8)


thresh = 80  # threshold in 0-100 scale


TAGGED_DATA_DIR = os.path.join("..", "data", "tagged_bert_small_toy")
assert os.path.isdir(TAGGED_DATA_DIR), f"You must run predict.ipynb before to have tagged data in {TAGGED_DATA_DIR}"

#// if os.path.exists("best_bert_finetuned_ner"):
#//     USE_BERT = True
#// else:
#//     cont = input("Pretrained BERT model best_bert_finetuned_ner eas not found... Continue w/o BERT tagging to populate the DB? [y/n] ")
#//     if cont.lower() == 'y':
#//         USE_BERT = False
#//     elif cont.lower() == 'n':
#//         print('ok bye')
#//         exit()
#//     else:
#//         print("option not recognized (not 'y' nor 'n')...")
#//         exit()

# ==============================================================================
# LOAD BERT-PREPROCESSED DATA AND COMPUTE BASE-SIMILARITY MATRIX
# ==============================================================================

data = {}  # map ID[int] : tagged product instance[dict]
id2market = {}  # map ID[int] : market we took product instance from[str]
market2id = {} # map market we took product instance from[str] : list of IDs
i = 0
for fname in os.listdir(TAGGED_DATA_DIR):
    with open(os.path.join(TAGGED_DATA_DIR, fname), "r", encoding='utf-8') as f:
        products = json.load(f)
        for prod in products:
            data[i] = prod
            id2market[i] = fname
            if fname not in market2id: 
                market2id[fname] = []
            market2id[fname].append(i)
            i += 1

texts = []  # raw texts of products
for _, v in sorted(data.items()):
    texts.append(v['product'])

# build base similarity matrix
print("building base similarity matrix...")
sim_matrix = process.cdist(texts, texts, dtype=np.int8, workers=8)
print("similarity matrix has shape", sim_matrix.shape)

# force similarity to be zero for products in same market
print("Zeroing out similarities for products in same market...")
for id_list in market2id.values():
    for id1 in tqdm(id_list):
        for id2 in id_list:
            sim_matrix[id1][id2] = 0

# compile numba function
build_edge_list(np.array([[1]]), 70)


# ==============================================================================
# REFINE SIMILARITY MATRIX
# ==============================================================================

# compile pairs2refine with small example
pairs2refine(np.array([[20, 80], [100, 20]], dtype=np.int8))

l = pairs2refine(sim_matrix)
for i, j in tqdm(l):
    sim_matrix[i][j] = similarity(data[i]['tags'], data[j]['tags'])
    sim_matrix[j][i] = sim_matrix[i][j]

# ==============================================================================
# CLUSTERIZE
# ==============================================================================

N = len(data)
assert sim_matrix.shape == (N, N)
n_clusters = 0
print("array of products' clusters")
clusters = - np.ones(N, dtype=int) #* clusters[prod of id N] is the cluster number
                            #! CONVENTION: VALID CLUSTER NUMBERS STARTING AT 0
cluster2markets = {}  #* cluster number: list of markets present in cluster

print("building list to sort")
n_edges, leftnodes, rightnodes, similarities = build_edge_list(sim_matrix, thresh)
edges = [(int(t[0]),int(t[1]),t[2]) for i, t in enumerate(zip(leftnodes, rightnodes, similarities)) if i < n_edges]


print(f"sorting valid edges (total of edges: {len(edges)})")
edges = sorted(edges, key=lambda t: t[2], reverse=True)

print("building clusters")
for e in tqdm(edges):
    # if both nodes already have a cluster, skip edge
    if clusters[e[0]] != -1 and clusters[e[1]] != -1:
        continue
    # if only one of the nodes has a cluster and the market of the other node is not yet 
    # represented in the cluster, add that unclustered node to the node
    if clusters[e[1]] != -1 and id2market[e[0]] not in cluster2markets[clusters[e[1]]]:
        clusters[e[0]] = clusters[e[1]]
        cluster2markets[clusters[e[1]]].append(id2market[e[0]])
        continue
    if clusters[e[0]] != -1 and id2market[e[1]] not in cluster2markets[clusters[e[0]]]:
        clusters[e[1]] = clusters[e[0]]
        cluster2markets[clusters[e[0]]].append(id2market[e[1]])
        continue
    # if both don't have a cluster, create new cluster and add both
    # NOTE: since entries for same market have been zeroed-out before starting the algorithm
    # and threshold > 0, then we know e[0] and e[1] are from different markets
    cluster = n_clusters
    n_clusters += 1
    clusters[e[0]] = cluster
    clusters[e[1]] = cluster
    cluster2markets[cluster] = [id2market[e[0]], id2market[e[1]]]

# do clustering for remaining products
for i, val in enumerate(clusters):
    if val == -1:
        clusters[i] = n_clusters
        n_clusters += 1

# ==============================================================================
# POPULATE DB
# ==============================================================================

TABLES = [ # listed in a deletion-friendly order (to avoid explicit cascade declarations)
    "mercado",
    "unidades_si",
    "tipo_dimensao",
    "tipo_produto",
    "instancia_produto"
]

user = input("Your PostgreSQL user: ")
password = getpass("Your PostgreSQL password: ")

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:5432/shopsmart")
tipo_dimensao_list = []  # will be used for bulk dump later
tipo_produto_list = []  # idem
instancia_produto_list = []  # idem

try:
    conn = psycopg2.connect(
        host="localhost",
        database="shopsmart",
        user=user,
        password=password  # enter your password!
    )
    cur = conn.cursor()

    # creating tables
    cur.execute("SELECT * FROM information_schema.tables WHERE table_name='tipo_produto';")
    tables_exist = cur.fetchone()
    if tables_exist is None:
        do = input("Tables not found. Create them now? [y/n] ")
        if do.lower() == 'n':
            print('ok bye')
            exit()
        elif do.lower() == 'y':
            with open(os.path.join("..", "data", "script.sql"), 'r') as f:
                print("importing tables from ../data/script.sql...")
                cur.execute(f.read())
                conn.commit()
                cur.execute("SELECT * FROM information_schema.tables WHERE table_name='tipo_produto';")
                tables_exist = cur.fetchone()
                assert tables_exist is None, "unfortunately we did not succeed in creating the files :("
            print('created')
        else:
            print("answer not 'y' nor 'n'... bye")
            exit()
    
    # resetting products (all tables except market one)
    cur.execute("SELECT * FROM tipo_produto;")
    instancia = cur.fetchone()
    LOAD_PRODS = True
    if instancia:
        do = input("Delete all product data and re-load? [y/n]")
        if do.lower() == 'n':
            print('ok')
            LOAD_PRODS = False
            exit()
        elif do.lower() == 'y':
            for table in filter(lambda s: s != "mercado", TABLES):
                cur.execute("DELETE FROM %s;", (table,))
            conn.commit()
            print('deleted')
        else:
            print("answer not 'y' nor 'n'... bye")
            exit()
    
    # resetting markets
    cur.execute("SELECT * FROM mercado;")
    instancia = cur.fetchone()
    LOAD_MARKETS = True
    if instancia:
        do = input("Delete all markets and re-load? [y/n]")
        if do.lower() == 'n':
            print('ok')
            LOAD_MARKETS = False
        elif do.lower() == 'y':
            cur.execute("DELETE FROM mercado;", (table,))
            conn.commit()
            print('deleted')
        else:
            print("answer not 'y' nor 'n'... bye")
            exit()

    # loading dimensions if not present
    cur.execute("SELECT * FROM unidades_si;")
    instancia = cur.fetchone()
    if instancia:
        print("It seems that unidades_si is already populated: skipping")
        print("Since this list is hard-coded anyway, feel free to manually change it if you want to change the table of unidades")
    else:
        print("Populating table of SI unities")
        cur.executemany(
            "INSERT INTO unidades_si(unidade_si) VALUES (%s);",
            [("kg",), ("L",), ("m",), ("m^2",), ("un",), ("(outra unidade)",)]  # ok, L is not SI but it is better then 0.001m^3 of juice
        )
        conn.commit()
        print("data inserted")
        

    # loading markets
    if LOAD_MARKETS:
        with open(os.path.join("..", "data", "dados_mercados.json"), "r", encoding="utf-8") as f:
            dados_mercados = json.load(f)
        for k, v in dados_mercados.items():
            cur.execute(
                "INSERT INTO mercado(m_id, nome_mercado, endereco, latitude, longitude) VALUES (%s, %s, %s, %s, %s)",
                (k, v["nome"], v["endereco"], v["latitude"], v["longitude"])
            )
        conn.commit()

    # loading products
    if LOAD_PRODS:
        # start by loading produts data from pickle
        market2products = {}
        for fname in os.listdir(".."):
            if fname.endswith(".pickle"):
                with open(os.path.join("..", fname), "rb") as f:
                    market2products[fname.replace(".pickle", "")] = pickle.load(f)
        print(list(market2products.keys()))
        #// # load NER-tagger?
        #// if USE_BERT:
        #//     ner = NERModel()
        
        visited_clusters2tpid = {}
        
        # recall that var clusters is an array where clusters[i] is cluster nb of prod i
        no_metadata_count = 0
        duplicates_count = 0  # count product instances that would be linked to same "product type' and in same market!"
        for prod_id, cluster in enumerate(clusters):
            prod_data = data[prod_id]
            m_id = id2market[prod_id].replace(".json", "")
            prod_metadata = None
            for x in market2products[m_id]:
                if x.description == prod_data["product"]:
                    prod_metadata = x
                    break
            if prod_metadata is None:
                no_metadata_count += 1
                continue  # to next product
            if cluster not in visited_clusters2tpid: # first visit
                # make product "representant" of that cluster and use it as tipo_produto
                #// if USE_BERT:
                nome_do_tipo = prod_data["product"]
                marca = prod_data["tags"].get("MAR", [""])[0]
                quantidade = prod_data["tags"].get("QUA", ["1"])[0]
                try:
                    quantidade = int(quantidade)
                except ValueError:
                    quantidade = 1
                detalhes = prod_metadata.details
                if "TAM" in prod_data["tags"]:
                    dim = re.sub(r"[\d,.\s]", "", prod_data["tags"]["TAM"][0]) # remove digits
                    dim = dim.lower().strip()
                    if dim == "kg":
                        pass
                    elif dim == "g":
                        dim = "kg"
                        quantidade /= 1000
                    elif dim == "l":
                        dim = "L"
                    elif dim == "m3" or dim == "m^3":
                        dim = "L"
                        quantidade *= 1000
                    elif dim == "dm3" or dim == "dm^3":
                        dim = "L"
                    elif dim == "ml":
                        dim = "L"
                        quantidade /= 1000
                    elif dim == "m":
                        pass
                    elif dim == "dm":
                        dim = "m"
                        quantidade /= 10
                    elif dim == "cm":
                        dim = "m"
                        quantidade /= 100
                    elif dim == "mm":
                        dim = "m"
                        quantidade /= 1000
                    elif dim == "m2" or dim == "m^2":
                        dim = "m^2"
                    elif dim == "dm2" or dim == "dm^2":
                        dim = "m^2"
                        quantidade /= 100
                    elif dim == "cm2" or dim == "cm^2":
                        dim = "m^2"
                        quantidade /= 10000
                    else:
                        dim = "(outra unidade)"
                else:
                    # it seems that the trained NER model does not use TAM for products counted as unities
                    dim = "un" 
                dim_id = uuid4()
                #? cur.execute(
                #?     "INSERT INTO tipo_dimensao(dim_id, unidade_si, valor) VALUES (%s, %s, %s)",
                #?     (dim_id, dim, quantidade)
                #? )
                tipo_dimensao_list.append((dim_id, dim, quantidade))
                tp_id = uuid4()
                #? cur.execute(
                #?     "INSERT INTO tipo_produto(tp_id, nome_do_tipo, marca, quantidade, dim_id, detalhes) VALUES (%s, %s, %s, %s, %s, %s)",
                #?     (tp_id, nome_do_tipo, marca, quantidade, dim_id, detalhes)
                #? )
                tipo_produto_list.append((tp_id, nome_do_tipo, marca, quantidade, dim_id, detalhes))
                #? conn.commit()
                visited_clusters2tpid[cluster] = tp_id
            else:
                # retrieve tp_id
                tp_id = visited_clusters2tpid[cluster]
            # check if product is really unique
            #? cur.execute("SELECT * FROM instancia_produto WHERE m_id='%s' AND tp_id='%s'", (m_id, tp_id))
            #? if cur.fetchone():
            #?    duplicates_count += 1
            #?    continue
            if len([prod for prod in instancia_produto_list if (prod[0], prod[1]) == (m_id, tp_id)]) > 0:
                duplicates_count += 1
                continue
            # insert product instance
            nome_produto = prod_data["product"]
            preco = prod_metadata.unitPrice
            disponibilidade = True  #! don't know
            logo_url = f"https://static.ifood-static.com.br/image/upload/t_high/pratos/{prod_metadata.logoUrl}"
            ultima_mudanca = datetime.now()
            #? cur.execute(
            #?     "INSERT INTO instancia_produto(m_id, tp_id, nome_produto, preco, disponibilidade, logo_url, ultima_mudanca) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            #?     (m_id, tp_id, nome_produto, preco, disponibilidade, logo_url, ultima_mudanca)
            #? )
            instancia_produto_list.append(
                (m_id, tp_id, nome_produto, preco, disponibilidade, logo_url, ultima_mudanca)
            )
        print(f"{no_metadata_count} products could not be associated to their metadata thus were skipped")
        print(f"{duplicates_count} duplicate product instances removed")

except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise
finally:
    if conn is not None:
        conn.close()
        print("Connection closed")


with engine.connect() as conn:
    if len(tipo_dimensao_list) > 0:
        print("tipo_dimensao:")
        tipo_dimensao_df = pd.DataFrame(tipo_dimensao_list, columns=["dim_id", "unidade_si", "valor"])
        print(len(tipo_dimensao_df), "items")
        print(tipo_dimensao_df.sample(5))
        tipo_dimensao_df.to_sql(name="tipo_dimensao", con=conn, if_exists="append", index=False)
    if len(tipo_produto_list) > 0:
        print("tipo_produto:")
        tipo_produto_df = pd.DataFrame(tipo_produto_list, columns=["tp_id", "nome_do_tipo", "marca", "quantidade", "dim_id", "detalhes"])
        print(len(tipo_produto_df), "items")
        print(tipo_produto_df.sample(5))
        tipo_produto_df.to_sql(name="tipo_produto", con=conn, if_exists="append", index=False)
    if len(instancia_produto_list) > 0:
        print("instancia_produto:")
        instancia_produto_df = pd.DataFrame(instancia_produto_list, columns=["m_id", "tp_id", "nome_produto", "preco", "disponibilidade", "logo_url", "ultima_mudanca"])
        print(len(instancia_produto_df), "items")
        print(instancia_produto_df.sample(5))
        instancia_produto_df.to_sql(name="instancia_produto", con=conn, if_exists="append", index=False)