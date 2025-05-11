from pathlib import Path

import chq.fs.ctf as ctf
from chq.fs.ctxfile import CTX_FILENAME, CTXFile
from chq.fs.util import create_dir

ORIGINAL_DIR = ".orig"
class Chall:
    path: Path
    def __init__(self, path: Path) -> None:
        self.path = path

    @property
    def ctf(self):
        return ctf.Ctf(self.path.parent)

    def init(self, allow_exists=True):
        create_dir(self.path, "challdir", allow_exists=allow_exists)

    def ensure_initialized(self):
        if not self.path.is_dir():
            raise FileNotFoundError(self.path)
