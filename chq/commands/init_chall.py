from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('name', type=str)
    parser.add_argument("--no-switch", dest="switch", action="store_const", const=False, default=True)
    parser.add_argument("--allow-exists", dest="allow_exists", action="store_const", const=True, default=False)

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    chall = ctx.ctf.get_chall(normalize(res.name))
    chall.init(allow_exists=res.allow_exists)
    if res.switch:
        ctx.set_and_save("chall", normalize(res.name))
    print(chall.path)

init_chall_command = SubCommand(
    "init-chall",
    _initializer,
    _handler,
    aliases=["init"]
)
