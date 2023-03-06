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

**Query API: Financial Data**
```
curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-02-21&end_date=2023-03-01&symbol=IBM&limit=3&page=1'
```
formatted output:
```
{
  "data": [
    {
      "close_price": "128.19",
      "date": "2023-03-01",
      "open_price": "128.90",
      "symbol": "IBM",
      "volume": "3760678"
    },
    {
      "close_price": "129.30",
      "date": "2023-02-28",
      "open_price": "130.55",
      "symbol": "IBM",
      "volume": "5143133"
    },
    {
      "close_price": "130.49",
      "date": "2023-02-27",
      "open_price": "131.42",
      "symbol": "IBM",
      "volume": "2761326"
    }
  ],
  "info": {
    "error": ""
  },
  "pagination": {
    "count": 7,
    "limit": 3,
    "page": 1,
    "pages": 3
  }
}
```

**Query API: Statistics Data**
```
curl -X GET 'http://localhost:5000/api/statistics?start_date=2023-02-21&end_date=2023-03-06&symbol=IBM'
```
formatted output:
```
{
  "data": {
    "average_daily_close_price": 130.07,
    "average_daily_open_price": 130.63,
    "average_daily_volume": 3562736,
    "end_date": "2023-03-06",
    "start_date": "2023-02-21",
    "symbol": "IBM"
  },
  "info": {
    "error": ""
  }
}
```

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
