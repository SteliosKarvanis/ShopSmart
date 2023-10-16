# Backend for ShopSmart

This is the backend of our ShopSmart project, which uses Flask as the web framework and PostgreSQL as the database management system.

## Overview

The backend of this project is responsible for serving data and handling requests from the frontend or other clients. Flask is used to create RESTful APIs and manage routes, while PostgreSQL is used as the database to store and manage data.

## Installation

Before running the backend, ensure you have the following prerequisites installed:

- Python (3.6+)
- PostgreSQL
- Pip (Python package manager)
- SQLAlchemy

1. Create and acitvate a virtual environment (optional but recommended)

   conda create --name backend-env
   conda activate backend-env

2. Install project dependencies
   conda install -r requirements.txt

3. Create a PostgreSQL database and configure the connection in 'config.py'

4. Run the backend server
   python app.py

## Configuration

Make sure to configure your databse connection and other environment related settings in the 'config.py' file

## API Endpoints

Document API endpoints and their funcitonalities here
Example: GET /api/resource

## Database Schema

Describe database schema here and include any necessary migration instructions

## Contributing

## License

## Contact
