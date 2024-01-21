from os import system
from .data.language import contexts
from llama_cpp import Llama
from langchain_community.llms import Ollama


class LanguageProcessor():
  model_server = "http://127.0.0.1:11434"
  models = {
    'nano': {
      'rank': 0,
      'label': 'dolphin-phi:2.7b-v2.6',
      'type': 'ollama'
    },
    'tiny': {
      'rank': 1,
      'label': 'dolphin-phi:2.7b-v2.6-q6_K',
      'type': 'ollama'
    },
    'base': {
      'rank': 2,
      'label': 'dolphin-mistral:7b-v2.6',
      'type': 'ollama'
    },
    'small': {
      'rank': 3,
      'label': 'dolphin-mistral:7b-v2.6-dpo-laser-q6_K',
      'type': 'ollama'
    },
    'medium': {
      'rank': 4,
      'label': '2x7b.Q4_K_M',
      'type': 'native'
    }
  }
  contexts = {
    'tiny': contexts.tiny,
    'base': contexts.base,
    'small': contexts.base,
    'medium': contexts.base
  }

  def __init__(self, model:str='base') -> None:
    self.size = model
    self.meta = self.models[model]
    if self.meta['type'] == 'ollama':
      self.model = Ollama(
        base_url=self.model_server,
        model=self.meta['label']
      )
    elif self.meta['type'] == 'native':
      self.model = Llama(
        model_path=f"./api/dexter/processor/models/data/language/{self.meta['label']}.gguf",
        n_ctx=32768,
        n_threads=16,
        n_gpu_layers=160
      )

  def prompt(self, tokens:str) -> str:
    context = self.contexts[self.size].context(tokens)
    if self.meta['type'] == 'ollama':
      response = self.model(context).strip()
      if self.size == 'nano' or self.size == 'tiny':
        if response.startswith('Dexter:'):
          response = "Dexter:".join(response.split("Dexter:")[1:])
        if response.startswith('Dex:'):
          response = "Dex:".join(response.split("Dex:")[1:])
      return response
    elif self.meta['type'] == 'native':
      output = self.model(
        context,
        max_tokens=670,
        stop=["<|im_end|>", "\n\nUser:"],
        echo=True
      )
      response = output['choices'][0]['text']\
        .replace(context, '')\
        .replace('<|im_start|>', '')\
        .replace('<|im_end|>', '')
      return response
