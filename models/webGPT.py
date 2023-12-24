from web.settings import BASE_DIR
from ..webGPT import ChatGPT

webGPT = ChatGPT(f"{BASE_DIR}/api/dexter/webGPT/chat.openai.com.cookies.json")


def input(text:str):
  prompt = text.strip()
  response = webGPT.chat(prompt).strip()

  if response.startswith("[DEXTER]:"):
    response = "[DEXTER]:".join(response.split("[DEXTER]:")[1:])

  return response
