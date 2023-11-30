# ShopSmart

To download the dependencies, run `pip install -r requirements.txt`

## Code Linting
To execute code style linting, run `make lint-python`

## Labeling Tool
To execute the labeling tool, run `python tools/labeling_tool.py --data={file with data}` from the project root

## Preparing the DB
### Requirements:
- PostgreSQL
- Python 3.9+ with the requirements listed in requirements.txt
### Steps
1. Download data with `utils/scrapping.py`. It must result in some pickle files in `./` and some json files in `data/raw/`
2. Train BERT using `train.ipynb`. It will save a modul under `best_bert_finetuned_ner`
3. Now that you have both BERT and raw data files, tag them using `predict.ipynb`. It will result in some JSON files under `data/tagged_bert` (rename it if necessary)
4. Manualy create and fill in `data/dados_mercados.json` in the following schema:
    ```
    {
        "id_mercado": {
            "nome": "...",
            "endereco": "...",
            "latitude": a float,
            "longitude": a float
        },
        ...
    }
    ```
    where `id_mercado` is like the names of the pickle/JSON corresponding to that market, **removing** only the file extension (`.json` or `.pickle`)
5. Create a database `shopsmart` under PostgreSQL
6. `cd` into `tools` (you must be there for this to work) and run `python populate_db.py`.
