from ..tables import PromptsModel
from core.library import (
  api,
  asyncio,
  parse_qsl,
  sync_to_async,
  AsyncJsonWebsocketConsumer
)


def create_new_prompt_process(req, *args, **kwargs):
  try:
    user = api.get_user(req)
    if user is None:
      return api.fail("Failed to authenticate user.")

    messages = api.get_json(req)['messages']
    prompt_text = ""
    for message in messages:
      msg_content = message['content'].replace('\n', ' ').strip()
      prompt_text += f"<|im_start|>{message['sender'].title()}\n{msg_content}<|im_end|>\n"

    prompt_process_object = PromptsModel.objects.create(
      user=user.data.uuid,
      prompt=prompt_text,
      potential_cta=messages[-1]['content']
    )
    return api.data(prompt_process_object.uuid)
  except Exception as exception:
    return api.error(exception)


class PromptProcessesConsumer(AsyncJsonWebsocketConsumer):

  async def connect(self, *args, **kwargs):
    super().connect()
    await self.accept()
    await self.update_prompt_status_periodically(
      prompt_id=dict(parse_qsl(self.scope['query_string'].decode('utf-8')))['promptId']
    )

  async def update_prompt_status_periodically(self, prompt_id:str, *args, **kwargs):
    while True:
      prompt_status = await self.check_prompt_status(prompt_id=prompt_id)
      await self.send_json(content=prompt_status)
      if prompt_status['status'] == 'finished':
        await self.close()
        break
      else:
        await asyncio.sleep(1)

  @sync_to_async
  def check_prompt_status(self, prompt_id:str, *args, **kwargs):
    prompt_object = PromptsModel.objects.get(uuid=prompt_id)
    prompt_status = {
      'status': prompt_object.status,
      'response': prompt_object.response if prompt_object.status == 'finished' else None
    }

    if prompt_object.status == "finished":
      prompt_object.delete()

    return prompt_status
