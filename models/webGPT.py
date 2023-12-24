from web.settings import BASE_DIR
from ..webGPT import ChatGPT
from ..contexts.dexter import instructions

webGPT = ChatGPT(f"{BASE_DIR}/api/dexter/webGPT/chat.openai.com.cookies.json")


def input(text:str):
  prompt = instructions(text).strip()
  response = webGPT.chat(prompt).strip()
  print(response)

  if response.startswith("[DEXTER]:"):
    response = "[DEXTER]:".join(response.split("[DEXTER]:")[1:])

  return response
