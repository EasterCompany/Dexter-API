from .webGPT import ChatGPT


def input(text:str):
  prompt = text.strip()
  response = ChatGPT(f"./webGPT/chat.openai.com.cookies.json").chat(prompt).strip()

  if response.startswith("[DEXTER]:"):
    response = "[DEXTER]:".join(response.split("[DEXTER]:")[1:])

  return response
