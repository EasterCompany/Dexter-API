import json
import secrets
import requests
import websocket
import threading
from sys import argv
from uuid import uuid4
from models.language import LanguageProcessor


class WorkerNode():
  worker_uid = (secrets.token_urlsafe(16) + str(uuid4())).replace('-', '')
  server_adr = "127.0.0.1:8995"
  ssl_enabled = False
  debug = True

  def __init__(self, debug=True) -> None:
    self.debug = debug
    if not debug:
      self.server_adr = "dexter.easter.company"
      self.ssl_enabled = True
    websocket.enableTrace(debug)
    self.socket = websocket.WebSocketApp(
      url=self.server_socket_uri(f"/api/ws/dexter/processor?clientId={self.worker_uid}"),
      on_error=self.on_error,
      on_close=self.on_close,
      on_message=self.on_message
    )
    self.socket.run_forever(reconnect=1 if debug else 10)

  def server_socket_uri(self, path='') -> str:
    return f"wss://{self.server_adr}{path}" if self.ssl_enabled else f"ws://{self.server_adr}{path}"

  def server_request_uri(self, path='') -> str:
    return f"https://{self.server_adr}{path}" if self.ssl_enabled else f"http://{self.server_adr}{path}"

  def on_error(self, ws:object, error:str) -> None:
    if self.debug:
      print(f"Socket Error Occurred: {error}")

  def on_close(self, ws:object, close_status_code:int, close_msg:str) -> None:
    if self.debug:
      print(f"Socket Connection closed: {close_msg}")

  def on_message(self, ws, message) -> None:
    data = json.loads(message)
    thread = threading.Thread(
      target=self.generate_prompt_response,
      name=f"prompt-process-{data['uuid']}",
      args=(
        data['uuid'],
        data['prompt']
      )
    )
    thread.daemon = False
    thread.start()

  def generate_prompt_response(self, prompt_uuid:str, prompt_message:str) -> str:
    requests.get(
      url=self.server_request_uri(f"/api/dexter/processor/response?clientId={self.worker_uid}"),
      headers={
        'Content-Type': 'application/json'
      },
      data=json.dumps({
        "prompt": prompt_uuid,
        "response": LanguageProcessor(model='base').prompt(prompt_message),
        "processor": self.worker_uid
      }).encode("utf-8")
    )


if __name__ == "__main__":
  debug = '-prd' not in argv
  node = WorkerNode(debug=debug)
