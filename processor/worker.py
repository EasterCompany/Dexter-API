import json
import secrets
import requests
import websocket
import threading
from uuid import uuid4
from models import mistral

worker_uid = (secrets.token_urlsafe(16) + str(uuid4())).replace('-', '')
server_adr = f"localhost:8995"
#server_adr = f"wss://dexter.easter.company"
server_socket_url = lambda ssl_enabled=False, uri_path='': f"wss://{server_adr}{uri_path}" if ssl_enabled else \
  f"ws://{server_adr}{uri_path}"
server_request_url = lambda ssl_enabled=False, uri_path='': f"https://{server_adr}{uri_path}" if ssl_enabled else \
  f"http://{server_adr}{uri_path}"


def on_error(ws:object, error:str) -> None:
  print(f"Socket Error Occurred: {error}")


def on_close(ws:object, close_status_code:int, close_msg:str) -> None:
  print(f"Socket Connection closed: {close_msg}")


def on_message(ws, message) -> None:
  data = json.loads(message)
  thread = threading.Thread(
    target=generate_prompt_response,
    name=f"prompt-processor-{data['uuid']}",
    args=(
      data['uuid'],
      data['prompt']
    )
  )
  thread.daemon = False
  thread.start()


def generate_prompt_response(prompt_uuid:str, prompt_message:str) -> str:
  requests.get(
    url=server_request_url(
      ssl_enabled=False,
      uri_path=f"/api/dexter/processor/response?clientId={worker_uid}"
    ),
    headers={
      'Content-Type': 'application/json'
    },
    data=json.dumps({
      "prompt": prompt_uuid,
      "response": mistral.prompt(prompt_message),
      "processor": worker_uid
    }).encode("utf-8")
  )


if __name__ == "__main__":
  websocket.enableTrace(True)
  socket = websocket.WebSocketApp(
    url=server_socket_url(
      ssl_enabled=False,
      uri_path=f"/api/ws/dexter/processor?clientId={worker_uid}"
    ),
    on_error=on_error,
    on_close=on_close,
    on_message=on_message
  )
  socket.run_forever(
    reconnect=3,
    origin="http://localhost:19006",
    host=server_request_url(ssl_enabled=False)
  )
