from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('--show-name', dest="show_name", action="store_const", const=True, default=False)

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    for chall in ctx.ctf.iter_chall():
        print(normalize(chall.path.name) if res.show_name else chall.path)

list_chall_command = SubCommand(
    "list-chall",
    _initializer,
    _handler
)
