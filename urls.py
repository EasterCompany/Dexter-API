from . import API
from .endpoints import chat

API.path(
  "chat/query",
  chat.query,
  "General purpose prompt endpoint"
)
