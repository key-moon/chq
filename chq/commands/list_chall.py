from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument("--ctf", nargs="?", const="", help="specify the ctf (default: current context)")
    parser.add_argument('--only-cur-ctx', dest="only_cur_ctx", action="store_const", const=True, default=False, help="only list the chall inside the current ctf")
    parser.add_argument('--full-path', '-p', dest="only_name", action="store_const", const=False, default=True, help="show full paths")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    if res.ctf is not None:
        ctfs = [ctx.root.get_ctf(normalize(res.ctf))]
    else:
        ctfs = ctx.root.iter_ctf()
    for ctf in ctfs:
        for chall in ctf.iter_chall():
            print(normalize(chall.path.name) if res.only_name else chall.path)

list_chall_command = SubCommand(
    "list-chall",
    _initializer,
    _handler,
    aliases=["list"],
    description="List challenges"
)
