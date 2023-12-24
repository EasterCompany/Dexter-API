from core.library import api
from ..models import llama2, mistral, webGPT


def query(req, *args, **kwargs):
  try:
    prompt = api.get_json(req)['prompt']
    response = webGPT.input(prompt).strip()
    return api.data(response)
  except Exception as exception:
    return api.error(exception)
