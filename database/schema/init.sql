CREATE TABLE UNIDADES_SI (
    unidade_si VARCHAR(16) PRIMARY KEY
);

CREATE TABLE TIPO_DIMENSAO (
    dim_id UUID PRIMARY KEY,
    unidade_si VARCHAR(16),
    valor VARCHAR(128),
    FOREIGN KEY (unidade_si) REFERENCES UNIDADES_SI(unidade_si)
);

CREATE TABLE TIPO_PRODUTO (
    tp_id UUID PRIMARY KEY,
    nome_do_tipo VARCHAR(128),
    marca VARCHAR(64),
    quantidade SMALLINT,
    dim_id UUID,
    detalhes VARCHAR(256),
    FOREIGN KEY (dim_id) REFERENCES TIPO_DIMENSAO(dim_id)
);

CREATE TABLE MERCADO (
    m_id UUID PRIMARY KEY,
    nome_mercado VARCHAR(64),
    endereco VARCHAR(256),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

CREATE TABLE INSTANCIA_PRODUTO (
    m_id UUID, 
    tp_id UUID,
    nome_produto VARCHAR(128),
    preco MONEY,
    disponibilidade BOOLEAN,
    logo_url VARCHAR(512),
    ultima_mudanca TIMESTAMP,
    FOREIGN KEY (m_id) REFERENCES MERCADO(m_id),
    FOREIGN KEY (tp_id) REFERENCES TIPO_PRODUTO(tp_id),
    PRIMARY KEY (m_id, tp_id)
);

CREATE TABLE ESPECIFICACAO(
    espec_id UUID PRIMARY KEY,
    content VARCHAR(128),
    tp_id UUID,
    FOREIGN KEY (tp_id) REFERENCES TIPO_PRODUTO(tp_id)
);
