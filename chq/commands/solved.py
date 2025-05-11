from argparse import ArgumentParser, Namespace
import os
from pathlib import Path
from chq.commands.get_current_ctf import get_ctf_and_chall

from chq.commands.parse_name import parse_chall_name
from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('chall_name', nargs="?", help="name of the challenge (default: ctx.chall)")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    
    ctf_name, chall_name = parse_chall_name(res.chall_name)
    if ctf_name is None or chall_name is None:
        ctf_name, chall_name = get_ctf_and_chall(ctx, Path.cwd().absolute())

    ctf_name, chall_name = normalize(ctf_name), normalize(chall_name)

    dest_ctf_name = normalize(ctf_name + "-solved")

    ctf = ctx.root.get_ctf(ctf_name)
    dest_ctf = ctx.root.get_ctf(dest_ctf_name)
    chall = ctf.get_chall(chall_name)
    dest_path = dest_ctf.path / chall_name

    ctf.ensure_initialized()
    dest_ctf.ensure_initialized()
    chall.ensure_initialized()

    chall.path.rename(dest_path)

    print(dest_path)

solved_command = SubCommand(
    "solved",
    _initializer,
    _handler,
    description="Move to the solved directory"
)
