from langchain.llms import Ollama

mistral = Ollama(
  base_url='http://127.0.0.1:11434',
  model='mistral'
)
