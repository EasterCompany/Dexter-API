from core.library import api
from ..models import mistral
from ..contexts.dexter import instructions


def query(req, *args, **kwargs):
  try:
    prompt = api.get_json(req)['prompt'].strip()
    struct = instructions(prompt)
    response = mistral.input(struct).strip()
    return api.data(response)
  except Exception as exception:
    return api.error(exception)
