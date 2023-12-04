# Backend for ShopSmart

This is the backend of our ShopSmart project, which uses Flask as the web framework and PostgreSQL as the database management system.

## Overview

The backend of this project is responsible for serving data and handling requests from the frontend or other clients. Flask is used to create RESTful APIs and manage routes, while PostgreSQL is used as the database to store and manage datavfrom the markets.

## Installation

Before running the backend, ensure you have the following prerequisites installed:

- Python (3.6+)
- PostgreSQL
- pgAdmin 4
- Pip (Python package manager)

### 1. Create and activate a virtual environment (optional but recommended)

Make sure you are in the backend directory not the project root

```bash
   cd backend
```

Create environment

```bash
   conda create --name backend-env
   conda activate backend-env
```

### 2. Install project dependencies

```bash
   conda install -r requirements.txt
```

#### If you are not using a conda environment, you can just install packages using pip

```bash
   pip install -r requirements.txt
```

#### 3. Create a PostgreSQL database and configure the connection in 'config.py'

Open pgAdmin 4, then create a new database in the first server of the Servers group and name it shopsmart by following the instructions: click on Servers group then click on the first server - likely named PostgreSQL 15, then it will open up a list of options and right click on Databases then create then Database... then type shopsmart in the Database field then click on save.

### 4. Run the backend server and start database

Still in the backend directory, open a terminal and run

```bash
   flask --app app run
```

to run the backend server.

To initialize the database, open a new terminal since the other is hosting the backend server and run if for the first time

```bash
   flask --app app init-db
   flask --app app fill-db
```

Otherwise, run

```bash
   flask --app app clear-db
   flask --app app fill-db
```

The idea behind this is that fill-db is a file which contains values to fill the tables in the sql schema which is updated daily.

## Configuration

Make sure to configure your database connection and other environment related settings in the 'config.py' file

## API Endpoints

### 1. Search Product Type

- **Endpoint:** `/server/search-product-type`
- **Method:** `GET`
- **Description:** This endpoint allows users to search for product types based on user input. It expects a JSON payload containing the key 'userSearch' for user input and returns a JSON response with a list of matching product types and associated information.

  **Parameters:**

  - None (Uses `request.json` for 'GET' method).

  **Returns:**

  - For successful searches:
    ```json
    {
        "productList": [
            {
                "name": str,
                "imageSampleUrl": str or None,
                "unity": str,
                "qtd": int,
                "unities": int,
                "tp_id": int
            },
            ...
        ]
    }
    ```
  - For invalid JSON or missing 'userSearch':
    ```json
    { "error": "Invalid JSON format" }
    ```
  - For an invalid request method:
    ```json
    { "error": "Invalid request method" }
    ```

### 2. Recommend Markets

- **Endpoint:** `/server/recommend-markets`
- **Method:** `GET`
- **Description:** This endpoint provides recommendations for markets based on user location and a list of desired products. It expects a JSON payload containing keys 'userLocation' and 'productList' for user location and a list of products, respectively. The endpoint returns a JSON response with recommended markets and relevant information.

  **Parameters:**

  - None (Uses `request.json` for 'GET' method).

  **Returns:**

  ```json
  {
      "Markets": [
          {
              "name": str,
              "distance-euclidean": float,
              "distance-haversine": float,
              "lat": float,
              "lon": float,
              "total": int,
              "cartInstances": [
                  {
                      "name": str,
                      "qte": int,
                      "unityPrice": str,
                      "subtotal": int
                  },
                  ...
              ],
              "cartContains": {
                  int (product_id): bool,
                  ...
              }
          },
          ...
      ]
  }
  ```

  - For invalid JSON or missing 'userLocation' or 'productList':
    ```json
    { "error": "Invalid JSON format" }
    ```
  - For an invalid request method:
    ```json
    { "error": "Invalid request method" }
    ```

## Database Schema

The provided SQL schema defines the structure of a database for managing information related to markets, product types, product dimensions, product instances, and product specifications.
