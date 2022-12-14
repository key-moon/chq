from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('--full-path', '-p', dest="only_name", action="store_const", const=False, default=True, help="show full paths")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    for ctf in ctx.root.iter_ctf():
        print(normalize(ctf.path.name) if res.only_name else ctf.path)

list_ctf_command = SubCommand(
    "list-ctf",
    _initializer,
    _handler,
    description="List ctfs"
)
