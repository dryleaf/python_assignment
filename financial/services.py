from sqlalchemy import func, select
from sqlalchemy_pagination import paginate
from financial.extensions import db
from financial.models.financial_data import FinancialData

def fetch_financial_data_by_fields_with_pagination(fields, paging):
  """Fetch financial data by fields with pagination from database

  Args:
      fields (dict): The fields to use for filtering
      paging (dict): The pagination information to fetch

  Returns:
      dict: The paginated data
  """
  query = FinancialData.query
  if fields["symbol"]:
    query = query.filter_by(symbol = fields["symbol"])
  if fields["start_date"]:
    query = query.filter(FinancialData.date >= fields["start_date"])
  if fields["end_date"]:
    query = query.filter(FinancialData.date <= fields["end_date"])
  
  query = paginate(query, page=paging["page"], page_size=paging["limit"])
  parsed_data = [x.as_dict() for x in query.items]
  
  return parsed_data, {"count": query.total, "page": paging["page"], "limit": paging["limit"], "pages": query.pages}

def compute_financial_data_stats_by_fields(fields):
  """Compute financial data statistics by fields

  Args:
      fields (dict): The field values to use for filtering the data.

  Returns:
      dict: The computed stats data
  """
  query = db.session.query(FinancialData.symbol,
    func.avg(FinancialData.open_price).label("average_daily_open_price"),
    func.avg(FinancialData.close_price).label("average_daily_close_price"),
    func.avg(FinancialData.volume).label("average_daily_volume")) \
  .filter(FinancialData.symbol == fields["symbol"],
    FinancialData.date.between(fields["start_date"], fields["end_date"])) \
  .group_by(FinancialData.symbol)
  
  result = query.first()
  
  if result:
    return {
      "start_date": fields["start_date"],
      "end_date": fields["end_date"],
      "symbol": result.symbol,
      "average_daily_open_price": round(float(result.average_daily_open_price), 2),
      "average_daily_close_price": round(float(result.average_daily_close_price), 2),
      "average_daily_volume": int(result.average_daily_volume)
    }
  else:
    f'No stats to show!!!'
