import json
import secrets
import websocket

client_id = secrets.token_urlsafe(128)
server_adr = f"ws://127.0.0.1:8995"
#server_adr = f"wss://dexter.easter.company"


def on_message(ws, message):
  data = json.loads(message)
  print(f"Received: {message}")
  resp = {
    "uuid": data["uuid"],
    "response": f"Hello, user! from {client_id}.",
    "processor": client_id
  }
  print(f"Responding: {resp}")
  ws.send(data=json.dumps(resp).encode('utf-8'), opcode=1)


def on_error(ws, error):
  print(f"Error occurred: {error}")


def on_close(ws, close_status_code, close_msg):
  print(f"[{close_status_code}] Connection closed: {close_msg}")


def on_open(ws):
  print("Connection opened")


if __name__ == "__main__":
  websocket.enableTrace(True)
  ws = websocket.WebSocketApp(
    f"{server_adr}/api/ws/dexter/processor?clientId={client_id}",
    on_open=on_open,
    on_error=on_error,
    on_close=on_close,
    on_message=on_message
  )
  ws.run_forever(
    reconnect=1,
    host="localhost:19006",
    suppress_origin=True
  )
