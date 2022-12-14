import os
from pathlib import Path

from chq.fs.ctf import Ctf
from chq.fs.ctxfile import CTX_FILENAME, CTXFile
from chq.fs.util import create_dir
from chq.util.path_normalize import normalize

CHQROOT_ENVVAR_NAME = "CHQ_ROOT"
DEFAULT_CHQROOT_DIRNAME = "chq"
class Root:
    path: Path
    def __init__(self, path: Path) -> None:
        self.path = path

    @property
    def ctxfile_path(self):
        return self.path / CTX_FILENAME
    @property
    def ctxfile(self):
        return CTXFile(self.ctxfile_path)

    def init(self, allow_exists=True):
        create_dir(self.path, "chqrootdir", allow_exists=allow_exists)
        self.ctxfile.init(allow_exists=allow_exists)

    def iter_ctf(self):
        for dir in self.path.iterdir():
            if not dir.is_dir(): continue
            yield Ctf(dir)

    def get_ctf(self, name: str):
        return Ctf(self.path / normalize(name))

def get_default_root():
    if CHQROOT_ENVVAR_NAME in os.environ:
        return Root(Path(os.environ[CHQROOT_ENVVAR_NAME]))
    else:
        return Root(Path("~").expanduser().joinpath(DEFAULT_CHQROOT_DIRNAME))

def get_initialized_default_root():
    root = get_default_root()
    root.init(allow_exists=True)
    return root
