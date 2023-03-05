import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from financial.models.financial_data import FinancialData

API_KEY = os.environ.get("API_KEY")
API_URL = os.environ.get("API_URL")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

engine = create_engine(SQLALCHEMY_DATABASE_URI, )
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def fetch_data(symbol):
  """Function to fetch financial data from external API

  Args:
      symbol (str): The company stocks code

  Returns:
      dict: Returns json data
  """
  
  data = {}
  
  response = requests.get(API_URL, params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": symbol,
    "apikey": API_KEY
  })
  
  if response.status_code == 200:
    data = response.json()
  
  return data

def process_data(symbol, data):
  """Processes the raw data by applying filters

  Args:
      symbol (str): The company stocks code
      data (dict): The json data containing financial data

  Returns:
      dict: Returns processed data
  """
  
  series = data.get("Time Series (Daily)", {})
  processed_data = []
  
  for date_str, values in series.items():
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if (datetime.today() - date).days > 14:
      # Ignore data that is greater than 14 days (2 weeks).
      continue
    
    open_price = values.get("1. open")
    close_price = values.get("4. close")
    volume = values.get("6. volume")
    
    processed_data.append(
      FinancialData(
        symbol=symbol,
        date=date.isoformat(),
        open_price=open_price,
        close_price=close_price,
        volume=volume))
  
  return processed_data

def save_data(data):
  """Saves the data in the database

  Args:
      data (dict): The financial data to be saved
  """
  session = Session()
  for d in data:
    if session.query(FinancialData).filter_by(symbol=d.symbol, date=d.date).first():
      # Skip if data exists in db
      continue
    session.add(d)
  session.commit()

def main():
  symbols = ['IBM', 'AAPL']
  for symbol in symbols:
    data = fetch_data(symbol)
    processed_data = process_data(symbol, data)
    save_data(processed_data)

if __name__ == '__main__':
  main()