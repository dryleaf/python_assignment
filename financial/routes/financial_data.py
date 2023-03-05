from flask import Blueprint, request
from financial import services
from financial.schemas.financial_data import FinancialDataResponseEntitySchema, InfoModel

bp = Blueprint('financial_data', __name__, url_prefix='/api')

@bp.route('/financial_data', methods=['GET'])
def index():
  """Financial data API controller

  Returns:
      Any: The type of financial data from the database
  """
  start_date = request.args.get('start_date') or None
  end_date = request.args.get('end_date') or None
  symbol = request.args.get('symbol') or None
  limit = request.args.get('limit') or 5
  page = request.args.get('page') or 1
  
  fields = {
    "symbol": symbol,
    "start_date": start_date,
    "end_date": end_date,
  }
  
  paging = {
    "limit": int(limit),
    "page": int(page)
  }
  
  response_entity = FinancialDataResponseEntitySchema()
  
  try:
    data, pagination = services.fetch_financial_data_by_fields_with_pagination(fields, paging)
    response_data = {"data": data, "pagination": pagination, "info": InfoModel(error='')}

    return response_entity.dump(response_data)
  except Exception as e:
    return response_entity.dump({data: [], pagination: {}, "info": InfoModel(error=e)})
