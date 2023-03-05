from pydantic import BaseModel
from typing import List
from financial.extensions import ma

class PaginationModel(BaseModel):
  count: int
  page: int
  limit: int
  pages: int

class InfoModel(BaseModel):
  error: str = ''

class StatisticsDataModel(BaseModel):
  start_date: str
  end_date: str
  symbol: str
  average_daily_open_price: float
  average_daily_close_price: float
  average_daily_volume: int

class FinancialDataModel(BaseModel):
  symbol: str
  date: str
  open_price: str
  close_price: str
  volume: str

class FinancialDataResponseEntitySchema(ma.Schema):
  class Meta:
    fields=('data', 'pagination', 'info')
  
  data = List[FinancialDataModel]
  pagination = PaginationModel
  info = InfoModel

class StatisticsDataResponseEntitySchema(ma.Schema):
  class Meta:
    fields=('data', 'info')
  
  data = List[StatisticsDataModel]
  info = InfoModel
