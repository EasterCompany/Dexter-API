import json
import redis
import secrets
import requests
import websocket
import threading
from sys import argv
from uuid import uuid4
from models.action import ActionProcessor
from models.language import LanguageProcessor

action_model = ActionProcessor()
language_model = LanguageProcessor()
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
REDIS_DB = redis.Redis(
  host=REDIS_HOST,
  port=REDIS_PORT,
  decode_responses=True
)


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
        data['prompt'],
        data['potential_cta']
      )
    )
    thread.daemon = False
    thread.start()

  def run_models(self, prompt_message:str, potential_cta:str) -> str:
    action_model_response = action_model.prompt(tokens=potential_cta)
    if action_model_response is not None and 'result' in action_model_response:
      return action_model_response['result']
    return language_model.prompt(tokens=prompt_message)

  def generate_prompt_response(self, prompt_uuid:str, prompt_message:str, potential_cta:str) -> str:
    if self.debug:
      prompt_response = self.run_models(prompt_message, potential_cta)
    else:
      try:
        prompt_response = self.run_models(prompt_message, potential_cta)
      except Exception as exception:
        prompt_response = f"Sorry, I encountered an error while processing your request: {exception}"

    requests.get(
      url=self.server_request_uri(f"/api/dexter/processor/response?clientId={self.worker_uid}"),
      headers={
        'Content-Type': 'application/json'
      },
      data=json.dumps({
        "prompt": prompt_uuid,
        "response": prompt_response,
        "processor": self.worker_uid
      }).encode("utf-8")
    )


if __name__ == "__main__":
  debug = '-prd' not in argv
  node = WorkerNode(debug=debug)
