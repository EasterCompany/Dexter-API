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

  def __init__(self, model:str='base') -> None:
    self.active_model = self.models[model]
    self.model = whisper.load_model(self.active_model)

  def transcribe(self, audio_file:str) -> str:
    transcription_data = self.model.transcribe(audio_file, fp16=self.gpu_enabled)
    transcription_text = transcription_data['text'].strip()
    return transcription_text
