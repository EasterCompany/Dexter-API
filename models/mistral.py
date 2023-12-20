from langchain.llms import Ollama

model_server = "http://127.0.0.1:11434"
fp16_version = "mistral:7b-instruct-v0.2-fp16"
prompt = Ollama(
  base_url=model_server,
  model=fp16_version
)
