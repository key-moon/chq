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
    def ctxfile_path(self):
        return self.path / CTX_FILENAME
    @property
    def ctxfile(self):
        return CTXFile(self.ctxfile_path)
    @property
    def ctf(self):
        return ctf.Ctf(self.path.parent)
    @property
    def origdir_path(self):
        return self.path / ORIGINAL_DIR

    def init(self, allow_exists=True):
        create_dir(self.path, "challdir", allow_exists=allow_exists)
        create_dir(self.origdir_path, "origdir", allow_exists=allow_exists)
        self.ctxfile.init(allow_exists=allow_exists)
