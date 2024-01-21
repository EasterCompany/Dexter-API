import time
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
  server_adr = "127.0.0.1:8999"
  ssl_enabled = False
  debug = True

  def __init__(self, debug=True) -> None:
    self.debug = debug
    self.connection_open = False
    if not debug:
      self.server_adr = "dexter.easter.company"
      self.ssl_enabled = True
    websocket.enableTrace(debug)
    self.socket = websocket.WebSocketApp(
      url=self.server_socket_uri(f"/api/ws/dexter/processor?clientId={self.worker_uid}"),
      on_open=self.on_open,
      on_error=self.on_error,
      on_close=self.on_close,
      on_message=self.on_message,
      keep_running=True
    )
    while True:
      if not self.connection_open:
        try:
          self.socket.close()
          self.socket.run_forever(reconnect=1 if debug else 3)
        except Exception as exception:
          print(exception)
          time.sleep(2)
      time.sleep(1)

  def server_socket_uri(self, path='') -> str:
    return f"wss://{self.server_adr}{path}" if self.ssl_enabled else f"ws://{self.server_adr}{path}"

  def server_request_uri(self, path='') -> str:
    return f"https://{self.server_adr}{path}" if self.ssl_enabled else f"http://{self.server_adr}{path}"

  def on_open(self, ws:object) -> None:
    if self.debug:
      print(f"Socket Connection Opened.")
    self.connection_open = True

  def on_error(self, ws:object, error:str) -> None:
    if self.debug:
      print(f"Socket Connection Error: {error}")

  def on_close(self, ws:object, close_status_code:int, close_msg:str) -> None:
    if self.debug:
      print(f"Socket Connection Closed: {close_msg}")
    self.connection_open = False

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
        prompt_response = f"Sorry, I encountered an error while processing your request:\n\n" +\
          f"""```\n{exception}\n```\n\n""" +\
          f"You might consider sending this error message to [contact@easter.company](mailto:contact@easter.company)"

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
  debug = 'local' in argv
  node = WorkerNode(debug=debug)
