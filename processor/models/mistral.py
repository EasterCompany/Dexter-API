from langchain.llms import Ollama
from contexts.dexter import context

model_server = "http://127.0.0.1:11434"
models = {
  'latest': 'mistral',
  'instruct-fp16': 'mistral:7b-instruct-v0.2-fp16'
}
model_interface = Ollama(
  base_url=model_server,
  model=models['latest']
)


def prompt(user_input:str):
  prompt = context(user_input.strip())
  response = model_interface(prompt).strip()
  if response.startswith('Dexter:'):
    response = "Dexter:".join(response.split("Dexter:")[1:])
  return response
