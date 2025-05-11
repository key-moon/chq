from argparse import ArgumentParser, Namespace
from os import getcwd
import os
from pathlib import Path
from chq.commands.get_current_ctf import get_ctf_and_chall
from chq.commands.parse_name import parse_chall_name

from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('chall_name', nargs="?", type=str, help="challenge to switch (default: current directory)")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())

    if res.chall_name is None:
        dir = Path.cwd()
        if len(dir.parents) < 2:
            raise Exception("")
        ctf_name, chall_name = normalize(dir.parent.name), normalize(dir.name)
    else:
        ctf_name, chall_name = parse_chall_name(res.chall_name)
        if ctf_name is None:
            ctf_name = ctx["ctf"]
        if chall_name is None:
            chall_name = ctx["chall"]
        ctf_name, chall_name = normalize(ctf_name), normalize(chall_name)

    ctf = ctx.root.get_ctf(ctf_name)
    chall = ctf.get_chall(chall_name)
    ctf.ensure_initialized()
    chall.ensure_initialized()

    ctx.set_and_save("ctf", ctf_name)

switch_command = SubCommand(
    "switch",
    _initializer,
    _handler,
    description=""
)
