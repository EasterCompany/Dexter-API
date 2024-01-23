from .data.language import contexts
from llama_cpp import Llama
from langchain_community.llms import Ollama


class LanguageProcessor():
  models = {
    'yokto': {
      'rank': 0,
      'type': 'ollama',
      'label': 'dolphin-phi:2.7b-v2.6-q2_K',
      'agents': 1,
      'parameters': 2.7,
      'quant_level': 2,
      'quant_method': 'K',
      'size': 1.2,
      'context': 'single'
    },
    'zepto': {
      'rank': 1,
      'type': 'ollama',
      'label': 'dolphin-phi:2.7b-v2.6-q4_0',
      'agents': 1,
      'parameters': 2.7,
      'quant_level': 4,
      'quant_method': '0',
      'size': 1.6,
      'context': 'single'
    },
    'atto': {
      'rank': 2,
      'type': 'ollama',
      'label': 'dolphin-phi:2.7b-v2.6-q6_K',
      'agents': 1,
      'parameters': 2.7,
      'quant_level': 6,
      'quant_method': 'K',
      'size': 2.3,
      'context': 'single'
    },
    'femto': {
      'rank': 3,
      'type': 'ollama',
      'label': 'dolphin-phi:2.7b-v2.6-q8_0',
      'agents': 1,
      'parameters': 2.7,
      'quant_level': 8,
      'quant_method': '0',
      'size': 3.0,
      'context': 'single'
    },
    'pico': {
      'rank': 4,
      'type': 'ollama',
      'label': 'dolphin-mistral:7b-v2.6-q2_K',
      'agents': 1,
      'parameters': 7.0,
      'quant_level': 2,
      'quant_method': 'K',
      'size': 3.1,
      'context': 'single'
    },
    'nano': {
      'rank': 5,
      'type': 'ollama',
      'label': 'dolphin-mistral:7b-v2.6-q4_0',
      'agents': 1,
      'parameters': 7.0,
      'quant_level': 4,
      'quant_method': '0',
      'size': 4.1,
      'context': 'multi'
    },
    'micro': {
      'rank': 6,
      'type': 'ollama',
      'label': 'dolphin-mistral:7b-v2.6-dpo-laser-q6_K',
      'agents': 1,
      'parameters': 7.0,
      'quant_level': 6,
      'quant_method': 'K',
      'size': 5.9,
      'context': 'multi'
    },
    'milli': {
      'rank': 7,
      'type': 'ollama',
      'label': 'dolphin-mistral:7b-v2.6-dpo-laser-q8_0',
      'agents': 1,
      'parameters': 7.0,
      'quant_level': 8,
      'quant_method': '0',
      'size': 7.7,
      'context': 'multi'
    },
    'centi': {
      'rank': 8,
      'type': 'native',
      'label': '2x7b.Q4_K_M',
      'agents': 2,
      'parameters': 7.0,
      'quant_level': 4,
      'quant_method': 'KM',
      'size': 7.2,
      'context': 'multi'
    },
    'deci': {
      'rank': 9,
      'type': 'native',
      'label': '2x7b.Q6_K',
      'agents': 2,
      'parameters': 7.0,
      'quant_level': 6,
      'quant_method': 'K',
      'size': 9.8,
      'context': 'multi'
    },
    'base': {
      'rank': 10,
      'type': 'native',
      'label': '2x7b.Q8_0',
      'agents': 2,
      'parameters': 7.0,
      'quant_level': 8,
      'quant_method': '0',
      'size': 12.7,
      'context': 'multi'
    }
  }
  context_types = {
    'single': contexts.single,
    'multi': contexts.multi
  }

  def __init__(self, model:str='nano') -> None:
    self.size = model
    self.meta = self.models[model]
    self.context = self.context_types[self.meta['context']]

    if self.meta['type'] == 'ollama':
      self.model = Ollama(
        base_url="http://127.0.0.1:11434",
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
    context = self.context.context(tokens)

    if self.meta['type'] == 'ollama':
      response = self.model(context).strip()
      if response.startswith('Dexter:'):
        response = "Dexter:".join(response.split("Dexter:")[1:])
      elif response.startswith('Dex:'):
        response = "Dex:".join(response.split("Dex:")[1:])
      return response

    elif self.meta['type'] == 'native':
      output = self.model(
        context,
        max_tokens=670,
        stop=["<|im_end|>", "\n\nUser:"],
        echo=False
      )
      response = output['choices'][0]['text']\
        .replace(context, '')\
        .replace('<|im_start|>', '')\
        .replace('<|im_end|>', '')
      return response
