from core.library import models, uuid, time


class PromptsModel(models.Model):
  ''' Contains records of prompts created by users, their status and response '''
  uuid = models.CharField(
    unique=True,
    default=uuid,
    null=False,
    blank=False,
    max_length=36,
    primary_key=True
  )
  user = models.CharField(
    null=False,
    blank=False,
    max_length=36
  )
  prompt = models.TextField(
    null=False,
    blank=False
  )
  response = models.TextField(
    null=True,
    blank=True
  )
  status = models.CharField(
    null=False,
    blank=False,
    default="queued",
    max_length=16
  )
  created = models.DateTimeField(
    null=False,
    blank=False,
    default=time.now
  )
  finished = models.DateTimeField(
    null=True,
    blank=True
  )
  processor = models.CharField(
    default="",
    max_length=64
  )
