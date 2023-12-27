import requests
from background_task import background
from web.settings import DEBUG, SECRET_DATA

processor_id = SECRET_DATA['SERVER_UID']
server_address = f"http://localhost:{SECRET_DATA['LOCAL_PORT']}" if DEBUG else \
  f"https://{SECRET_DATA['SERVER_URL']}"


@background(schedule=1)
def claim_process():
  try:
    response = requests.get(f"{server_address}/api/dexter/processor/claim")
    response.raise_for_status()
  except requests.exceptions.RequestException as exception:
    print(f"An error occurred while claiming a process: {exception}")
    return None



