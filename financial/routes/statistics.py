from flask import Blueprint, request
from financial import services
from financial.schemas.financial_data import InfoModel, StatisticsDataResponseEntitySchema

bp = Blueprint('sta', __name__, url_prefix='/api')

@bp.route('/statistics', methods=['GET'])
def index():
  """The Statistics API controller

  Returns:
      Any: The compute stats on the financial data
  """
  start_date = request.args.get('start_date')
  end_date = request.args.get('end_date')
  symbol = request.args.get('symbol')
  
  fields = {
    "symbol": symbol,
    "start_date": start_date,
    "end_date": end_date,
  }
  response_entity = StatisticsDataResponseEntitySchema()
  
  try:
    data = services.compute_financial_data_stats_by_fields(fields)
    response_data = {"data": data, "info": InfoModel(error='')}

    return response_entity.dump(response_data)
  except Exception as e:
    return response_entity.dump({data: [], "info": InfoModel(error=e)})
