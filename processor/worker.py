import json
import secrets
import websocket

client_id = secrets.token_urlsafe(16)
server_adr = f"ws://127.0.0.1:8995"
#server_adr = f"wss://dexter.easter.company"


def on_message(ws, message):
  data = json.loads(message)
  resp = json.dumps({
    "uuid": data["uuid"],
    "response": f"Hello, user! from {client_id}.",
    "processor": client_id
  }).encode("utf-8")
  ws.send_bytes(data=resp)


def on_error(ws, error):
  print(f"Error occurred: {error}")


def on_close(ws, close_status_code, close_msg):
  print(f"[{close_status_code}] Connection closed: {close_msg}")


if __name__ == "__main__":
  websocket.enableTrace(True)
  socket = websocket.WebSocketApp(
    f"{server_adr}/api/ws/dexter/processor?clientId={client_id}",
    on_error=on_error,
    on_close=on_close,
    on_message=on_message
  )
  socket.run_forever(
    reconnect=1,
    origin="http://localhost:19006",
    host="http://localhost:8995"
  )
