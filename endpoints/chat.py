from core.library import api
from ..ollama.mistral import mistral


def query(req, *args, **kwargs):
  try:
    user_input = api.get_json(req)
    dexter_response = mistral(user_input['prompt']).strip()
    return api.data(dexter_response)
  except Exception as exception:
    return api.error(exception)
