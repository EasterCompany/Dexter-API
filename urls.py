from . import API
from .endpoints import prompt, processor

API.path(
  "prompt",
  prompt.create_new_prompt_process,
  "Creates a prompt process and returns id for streaming process status"
)

API.socket(
  "prompt",
  prompt.PromptProcessesConsumer,
  "Streams prompt process status & data back to the user client"
)

API.socket(
  "processor",
  processor.ProcessorConsumer,
  "Streams prompt to the processor and receives responses"
)
