"""Holds function eval_clusterization to evaluate a clusterization method

call me from inside tools/
"""

import os
import json
from thefuzz import fuzz as tfuzz  # string similarities
from rapidfuzz import process, fuzz
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from numba import njit
from datetime import datetime
from itertools import combinations


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
    return leftnodes, rightnodes, similarities


@njit
def pairs2refine(m, thresh=70):
    l = []
    for i in range(len(m)):
        for j, val in enumerate(m[i][i+1:]):
            if thresh <= val < 100:
                l.append((i,j))
    return l


def eval_clusterization(similarity, thresh):
    """does clusterization and generate 'report'

    Args:
        similarity (callable): function receiving two dicts of tags from ../utils/ner.p's 
                               NERModel and returning similarity in 0-100 range
        thresh (numpy.int8): similarity threshold
    """

    RESULTS_DIR = os.path.join(
        "..", "data", "eval_clustering", 
        # datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"),
        similarity.__name__ + "_" + str(thresh)
    )
    if os.path.exists(RESULTS_DIR):
        print(f"\033[93mIt seems this combination has already been evaluated (see {RESULTS_DIR}).\033[0m")
        return
    else:
        os.makedirs(RESULTS_DIR)

    TAGGED_DATA_DIR = os.path.join("..", "data", "tagged_bert")
    assert os.path.isdir(TAGGED_DATA_DIR), f"You must run predict.ipynb before to have tagged data in {TAGGED_DATA_DIR}"

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
    clusters = - np.ones(N, dtype=int) # clusters[prod of id N] is the cluster number
                                #! CONVENTION: VALID CLUSTER NUMBERS STARTING AT 0
    cluster2markets = {}  # cluster number: list of markets present in cluster

    print("building list to sort")
    leftnodes, rightnodes, similarities = build_edge_list(sim_matrix, thresh)
    edges = [(int(l),int(r),s) for l,r,s in zip(leftnodes, rightnodes, similarities)]

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
    # EVALUATE
    # ==============================================================================

    results = {
        "nb_clusters": int(max(clusters) + 1)
    }

    cluster_sizes = [len(val) for val in cluster2markets.values()] + \
                    [1 for _ in range(max(clusters) - len(cluster2markets))]
                    # this 2nd term is because singletons (clusters of 1 elem) are not in clisters2markets
    sns.histplot(cluster_sizes).figure.savefig(
        os.path.join(RESULTS_DIR, "cluster_sz_hist.png")
    )
    plt.close()

    with open(os.path.join(RESULTS_DIR, "examples.txt"), "w", encoding='utf-8') as f:
        for cluster in np.random.choice(max(clusters), 10):
            products_ids = [i for i, c in enumerate(clusters) if c == cluster]
            f.write(f"Cluster #{cluster}:\n")
            for pid in products_ids:
                f.write("\t" + texts[pid] + "\n")

    min_sims_in_cl = []
    for cluster in tqdm(np.random.choice(max(clusters), 10000)):
        products_ids = [i for i, c in enumerate(clusters) if c == cluster]
        min_sim = 999999
        for p1, p2 in combinations(products_ids, 2):
            if sim_matrix[min(p1, p2)][max(p1, p2)] < min_sim:
                min_sim = sim_matrix[min(p1, p2)][max(p1, p2)]
        if min_sim < 999999:  # can be == 999999 for clusters of 1 element (singletons)
            min_sims_in_cl.append(min_sim)
    plot = sns.histplot(min_sims_in_cl)
    plot.figure.savefig(
        os.path.join(RESULTS_DIR, "min_intracluster_sim_hist.png")
    )
    plt.close()

    results["percent_min_intracluster_sim_lt_threshold"] = 100*sum([x < thresh for x in min_sims_in_cl])/len(min_sims_in_cl)

    clusters_subset = np.random.choice(max(clusters), 1000)
    clusters_prods = [[i for i, c in enumerate(clusters) if c == cluster] for cluster in clusters_subset]

    # inter-cluster
    inter_sims = []
    for i, prods in enumerate(clusters_prods):
        rows = prods
        columns = []
        for j, other_prods in enumerate(clusters_prods):
            if j == i:
                continue
            columns += other_prods
        intersim_matrix = sim_matrix[np.ix_(rows, columns)]
        inter_sims += intersim_matrix.flatten().tolist()

    # intra-cluster
    intra_sims = []
    for prods in clusters_prods:
        intrasim_matrix = sim_matrix[np.ix_(prods, prods)]
        idxs = np.tril_indices(len(intrasim_matrix), -1) # only elements below diagonal (including diagonal, intracluster similarity distribution would be biased)
        intra_sims += intrasim_matrix[idxs].tolist()
    
    plot = sns.kdeplot({"intra-cluster": intra_sims, "inter-cluster": inter_sims}, common_norm=False)
    plot.figure.savefig(
        os.path.join(RESULTS_DIR, "intra_and_inter_cluster_sims.png")
    )
    plt.close()

    with open(os.path.join(RESULTS_DIR, "summary.json"), "w") as f:
        json.dump(results, f)

    print(f"\033[92mResults have been written to {RESULTS_DIR}\033[0m")
