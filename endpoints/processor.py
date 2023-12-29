from ..tables import PromptsModel
from core.library import (
  time,
  asyncio,
  parse_qsl,
  database_sync_to_async,
  AsyncJsonWebsocketConsumer
)


class ProcessorConsumer(AsyncJsonWebsocketConsumer):

  async def connect(self, *args, **kwargs):
    await self.accept()
    self.query_params = dict(parse_qsl(self.scope['query_string'].decode('utf-8')))
    self.processor_id = self.query_params['clientId']
    print(f"\nConnected to processor: {self.processor_id[:24]}...\n")
    await self.scan_records_periodically()

  def websocket_disconnect(self, message):
    print(f"\nDisconnected from processor: {self.processor_id[:24]}...\n")
    self.undesignated_processes()

  async def send_json(self, content, close=False):
    print(f"\nSending: {content}\n")
    await super().send(text_data=await self.encode_json(content), close=close)

  async def receive(self, text_data=None, bytes_data=None):
    print(f"\nReceiving: {text_data} {bytes_data}\n")
    super().receive()

  async def receive_json(self, content):
    print(f"\nReceiving: {content}\n")
    super().receive_json()

  async def scan_records_periodically(self, *args, **kwargs):
    while True:
      payload = await self.designate_process()
      if payload is not None:
        await self.send_json(content=payload)
      await asyncio.sleep(0.25)

  @database_sync_to_async
  def undesignated_processes(self, *args, **kwargs):
    records = PromptsModel.objects.filter(processor=self.processor_id)
    for record in records:
      if record.status != 'finished':
        record.status = 'queued'
        record.processor = ''
        record.save()

  @database_sync_to_async
  def designate_process(self, *args, **kwargs):
    undesignated_processes = PromptsModel.objects.filter(processor="").order_by('created')
    if undesignated_processes.count() == 0:
      return None

    process = undesignated_processes.first()
    process.processor = self.processor_id
    process.status = "processing"
    process.save()

    worker_payload = {
      "uuid": process.uuid,
      "prompt": process.prompt
    }
    return worker_payload

  @database_sync_to_async
  def update_process(self, uuid, processor, response):
    process = PromptsModel.objects.get(
      uuid=uuid,
      processor=processor
    )
    process.status = "finished"
    process.response = response
    process.finished = time.now()
    process.save()
    return
