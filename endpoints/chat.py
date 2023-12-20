from core.library import api
from ..models import mistral


def query(req, *args, **kwargs):
  try:
    user_input = api.get_json(req)['prompt']
    dexter_response = mistral.prompt(user_input).strip()
    return api.data(dexter_response)
  except Exception as exception:
    return api.error(exception)
