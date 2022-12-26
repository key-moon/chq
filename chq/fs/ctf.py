from pathlib import Path

import chq.fs.root as root
from chq.fs.chall import Chall
from chq.fs.ctxfile import CTX_FILENAME, CTXFile
from chq.fs.util import create_dir
from chq.util.path_normalize import normalize

class Ctf:
    path: Path
    def __init__(self, path: Path) -> None:
        self.path = path

    @property
    def ctxfile_path(self):
        return self.path / CTX_FILENAME
    @property
    def ctxfile(self):
        return CTXFile(self.ctxfile_path)
    @property
    def root(self):
        return root.Root(self.path.parent)

    def init(self, allow_exists=True):
        create_dir(self.path, "ctfdir", allow_exists=allow_exists)
        self.ctxfile.init(allow_exists=allow_exists)

    def ensure_initialized(self):
        if not self.path.is_dir():
            raise FileNotFoundError(self.path)
        self.ctxfile.ensure_initialized()

    def iter_chall(self):
        for dir in self.path.iterdir():
            if not dir.is_dir(): continue
            yield Chall(dir)

    def get_chall(self, name: str):
        return Chall(self.path / normalize(name))
