## Project description
This project has to main objectives:
- Fetch financial raw data from an external API, process it and save the data on the database.
- To create an API and display the Fetched financial data, with pagination and be able to compute some statistics on the financial data.

## Tech stack
- Python 3
- Flask
- PostgreSQL
- Docker
- Linux/Unix

## Running the App
**Starting**
```
docker-compose up
```

**Access the financial API app container**
```
docker exec -it python_assignment_financial_1 bash
```

**Define Variables to Run the get_raw_data.py script**
```
export API_URL=https://www.alphavantage.co/query
export API_KEY=<api key>
export SQLALCHEMY_DATABASE_URI=postgresql://<user>:<password>@db/<database name>
```

**Execute get_raw_data.py script**
```
python get_raw_data.py
```
- After this, the data is inserted in the database.

**Stopping**
```
docker-compose down
```

**Environment Variables**
I created a local environment file called `.env` for local development.
```
API_URL=https://www.alphavantage.co/query
API_KEY=<api key>
POSTGRES_HOST=db
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database name>
SECRET_KEY=<random string>
SQLALCHEMY_DATABASE_URI=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}/${POSTGRES_DB}
```

## How to maintain the API key
- Keep the API key safe and only use for environment variable configuration in deployment scenarios.
- Never store the API key in version control.
- Use separate API keys for development and production environments.
- It should be confidential.
