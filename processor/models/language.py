import time
from langchain.llms import Ollama
from contexts.dexter import context


class LanguageProcessor():
  model_server = "http://127.0.0.1:11434"
  active_model = None
  models = {
    'nano': 'phi:latest',
    'tiny': 'tinyllama:latest',
    'base': 'mistral:latest',
    'small': 'mixtral:latest'
  }

  def __init__(self, model:str='tiny') -> None:
    self.active_model = self.models[model]
    self.model = Ollama(
      base_url=self.model_server,
      model=self.active_model
    )

  def prompt(self, tokens:str) -> str:
    tokens = tokens.strip()
    token_context = context(tokens)
    response = self.model(token_context).strip()
    if response.startswith('Dexter:'):
      response = "Dexter:".join(response.split("Dexter:")[1:])
    return response


if __name__ == '__main__':
  engine = LanguageProcessor(model='tiny')
  prompt = "Hello, who are you and what do you do?"
  print(f"Sending prompt '{prompt}'")
  t0 = time.time()
  response = engine.prompt(tokens=f"User: {prompt}")
  t1 = time.time() - t0
  print(f"Received response '{response}'")
  print(f"Time taken: {t1}")
