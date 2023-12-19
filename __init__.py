from core.library import Path, dirname, realpath, api


class _API(api.UniversalAPI):
  NAME = Path(dirname(realpath(__file__))).parts[-1]

  def __init__(self) -> None:
    super().__init__()


API = _API()
