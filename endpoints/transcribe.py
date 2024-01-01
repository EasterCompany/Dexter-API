import numpy as np
from core.library import api
from ..processor.models.speech import SpeechRecognition


def transcribe_audio(req, *args, **kwargs):
  try:
    user = api.get_user(req)
    if user is None:
      return api.fail("Failed to authenticate user.")

    in_memory_file = req.FILES['file'].read()
    audio_array = np.frombuffer(in_memory_file, np.int8).flatten().astype(np.float32) / 32768.0
    engine = SpeechRecognition()
    transcription = engine.transcribe(audio_array)

    return api.data(transcription)
  except Exception as exception:
    return api.error(exception)
