from core.library import api
from ..ollama.mistral import mistral


def query(req, *args, **kwargs):
  try:
    user_input = api.get_json(req)
    return api.data(mistral(user_input['prompt']))
  except Exception as exception:
    return api.error(exception)
