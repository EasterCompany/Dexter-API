# Universal API __init__.py
#   Edit this file to configure your API

# Overlord library
from core.library import Path, dirname, realpath, api


class _API(api.UniversalAPI):

  # API.NAME represents which endpoint the urls for this API will be based on
  # for example: .../api/api_name/foobar
  NAME = Path(dirname(realpath(__file__))).parts[-1]

  def __init__(self) -> None:
    super().__init__()


# Exported Interface
API = _API()
