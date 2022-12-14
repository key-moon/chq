from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('name', type=str, help="name of the ctf")
    parser.add_argument("--only-init", dest="only_init", action="store_const", const=True, default=False, help="don't switch context after the initialization")
    parser.add_argument('--allow-exists', dest="allow_exists", action="store_const", const=True, default=False, help="don't stop the initialization even if the directory already exists")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    ctf = ctx.root.get_ctf(normalize(res.name))
    ctf.init(allow_exists=res.allow_exists)
    if not res.only_init:
        ctx.set_and_save("ctf", normalize(res.name))
    print(ctf.path)

init_ctf_command = SubCommand(
    "init-ctf",
    _initializer,
    _handler,
    description="Initialize a ctf"
)
