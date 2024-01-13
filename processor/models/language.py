import time
from langchain.llms import Ollama
from .contexts.language import context


class LanguageProcessor():
  model_server = "http://127.0.0.1:11434"
  active_model = None
  models = {
    'tiny': 'tinyllama:latest',
    'micro': 'phi:latest',
    'base': 'mistral:latest',
    'small': 'mixtral:latest',
    'medium': 'dolphin-mixtral:latest'
  }

  def __init__(self, model:str='base') -> None:
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
    if response.startswith('Dex:'):
      response = "Dex:".join(response.split("Dex:")[1:])
    return response
