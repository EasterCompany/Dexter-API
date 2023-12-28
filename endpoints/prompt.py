import asyncio
from urllib.parse import parse_qsl
from asgiref.sync import sync_to_async
from ..models import mistral
from ..tables import PromptsModel
from ..contexts.dexter import instructions
from core.library import api, AsyncJsonWebsocketConsumer


def query(req, *args, **kwargs):
  try:
    prompt = api.get_json(req)['prompt'].strip()
    struct = instructions(prompt)
    response = mistral.input(struct).strip()
    return api.data(response)
  except Exception as exception:
    return api.error(exception)


def create_new_prompt_process(req, *args, **kwargs):
  try:
    user = api.get_user(req)
    if user is None:
      return api.fail("Failed to authenticate user.")
    prompt_text = api.get_json(req)['prompt'].strip()
    prompt_process_object = PromptsModel.objects.create(
      user=user.data.uuid,
      prompt=prompt_text
    )
    return api.data(prompt_process_object.uuid)
  except Exception as exception:
    return api.error(exception)


class PromptProcessesConsumer(AsyncJsonWebsocketConsumer):
  keep_alive = True
  prompt_id = None
  current_status = None

  async def connect(self, *args, **kwargs):
    super().connect()
    self.query_params = dict(parse_qsl(self.scope['query_string'].decode('utf-8')))
    self.prompt_id = self.query_params['promptId']
    await self.accept()
    await self.update_prompt_status_periodically()

  async def disconnect(self, *args, **kwargs):
    super().disconnect()

  async def update_prompt_status_periodically(self, *args, **kwargs):
    while self.keep_alive:
      await self.update_prompt_status()
      await asyncio.sleep(0.25)

  async def update_prompt_status(self, *args, **kwargs):
    prompt_object = await self.get_prompt_object()
    if prompt_object is None:
      return await self.disconnect()

    self.current_status = prompt_object.status
    await self.send_json(
      content={
        'status': self.current_status,
        'response': prompt_object.response if prompt_object.status == 'finished' else None
      }
    )

    if self.current_status == "finished":
      prompt_object.delete()
      await self.disconnect()

  @sync_to_async
  def get_prompt_object(self, *args, **kwargs):
    if self.prompt_id is not None:
      return PromptsModel.objects.get(uuid=self.prompt_id)
    return None
