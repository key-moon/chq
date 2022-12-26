
import json
from pathlib import Path
from typing import Any, Dict

from chq.fs.util import create_file

def _check_data(dic: Any):
    if not isinstance(dic, dict) or any([not isinstance(val, str) for val in dic.values()]):
        raise TypeError("type of the configuration object should be Dict[str, str]")

def _serialize(dic: Dict[str, str]) -> str:
    _check_data(dic)
    return json.dumps(dic)

def _deserialize(s: str) -> Dict[str, str]:
    dic = json.loads(s)
    _check_data(dic)
    return dic

CTX_FILENAME = ".ctx"
_DEFAULT_CTXFILE_CONTENT = "{}"
class CTXFile:
    path: Path
    def __init__(self, path: Path) -> None:
        self.path = path
    
    def init(self, allow_exists=False):
        create_file(self.path, content=_DEFAULT_CTXFILE_CONTENT, name="ctxfile", allow_exists=allow_exists)

    def ensure_initialized(self):
        self._check_exists()

    def _check_exists(self):
        if not self.path.is_file():
            raise FileNotFoundError(f"file not found at {self.path}")

    def get_content(self):
        self._check_exists()
        return _deserialize(self.path.read_text())

    def set_content(self, content: Dict[str, str]):
        self._check_exists()
        self.path.write_text(_serialize(content))        
