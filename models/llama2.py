from langchain.llms import Ollama

model_server = "http://127.0.0.1:11434"
models = {
  'uncensored': 'llama2-uncensored'
}

input = Ollama(
  base_url=model_server,
  model=models['uncensored']
)
