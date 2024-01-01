import subprocess
from core.library import uuid, api, FileSystemStorage
from ..processor.models.speech import SpeechRecognition


def transcribe_audio(req, *args, **kwargs):
  try:
    user = api.get_user(req)
    if user is None:
      return api.fail("Failed to authenticate user.")

    data = req.FILES['file']
    tmp_data_name = f'{uuid()}{data.name}'
    FileSystemStorage(location='/tmp').save(tmp_data_name, data)
    engine = SpeechRecognition(model='base')
    transcription = engine.transcribe(f'/tmp/{tmp_data_name}')

    return api.data(transcription)
  except Exception as exception:
    return api.error(exception)


def convert_webm_to_flac(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-vn', '-c:a', 'flac', output_file]
    subprocess.run(command, check=True)
