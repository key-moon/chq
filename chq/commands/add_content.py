from argparse import ArgumentParser, Namespace
import os
from pathlib import Path
import shutil
import tempfile
from chq.commands.get_current_ctf import get_ctf_and_chall

from chq.commands.parse_name import parse_chall_name
from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument("files", nargs="*", help="files to copy")
    parser.add_argument("--extract", "-x", nargs="+", default=[], help="files to extract")
    parser.add_argument("--extract-raw", "-X", dest="extract_raw", nargs="+", default=[], help="files to extract(without recursive digging)")
    parser.add_argument('--chall', nargs="?", help="name of the challenge")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    
    ctf_name, chall_name = parse_chall_name(res.chall)
    if ctf_name is None or chall_name is None:
        ctf_name, chall_name = get_ctf_and_chall(ctx, Path.cwd().absolute())
    
    ctf = ctx.root.get_ctf(ctf_name)
    chall = ctf.get_chall(chall_name)
    ctf.ensure_initialized()
    chall.ensure_initialized()

    file_paths = [Path(file) for file in res.files]
    extract_paths = [Path(file) for file in res.extract]
    extract_raw_paths = [Path(file) for file in res.extract_raw]
    for path in file_paths + extract_paths:
        if not path.exists():
            raise FileNotFoundError(path)
    
    for path in file_paths:
        shutil.copy(path, chall.path)

    for path, do_rec in [(p, True) for p in extract_paths] + [(p, False) for p in extract_raw_paths]:
        dir = Path(tempfile.mkdtemp())
        # TODO: check the file name to avoid zipslip
        shutil.unpack_archive(path, dir)
        while do_rec and dir.is_dir():
            if len(list(dir.iterdir())) != 1 or not next(dir.iterdir()).is_dir():
                break
            dir = next(dir.iterdir())
        shutil.copytree(dir, chall.path, dirs_exist_ok=True)

add_content_command = SubCommand(
    "add-content",
    _initializer,
    _handler,
    aliases=["add"],
    description="Add file to the challenge"
)
