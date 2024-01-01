import os
import time
import torch
import whisper
from pathlib import Path
from os.path import dirname, realpath


class SpeechRecognition():
  gpu_enabled = torch.cuda.is_available()
  model_directory = f"{Path(dirname(realpath(__file__)))}/data/audio"
  active_model = None
  models = {
    'tiny': f"{model_directory}/tiny.en.pt",
    'base': f"{model_directory}/base.en.pt",
    'small': f"{model_directory}/small.en.pt"
  }

  def __init__(self, model:str='tiny') -> None:
    self.active_model = self.models[model]
    self.model = whisper.load_model(self.active_model)

  def transcribe(self, audio_file_path:str) -> str:
    transcription_data = self.model.transcribe(audio_file_path, fp16=self.gpu_enabled)
    transcription_text = transcription_data['text'].strip()
    return transcription_text


if __name__ == '__main__':
  engine = SpeechRecognition(model='tiny')
  test_file_dir = f"{engine.model_directory}/tests"
  test_files = os.scandir(test_file_dir)
  for index, test_file in enumerate(test_files):
    if not test_file.is_file():
      continue
    t0 = time.time()
    print(f"\nTest File [{test_file.name}]")
    print(engine.transcribe(f"{test_file_dir}/{test_file.name}"))
    print("Time Spent: ", time.time() - t0, "\n")
