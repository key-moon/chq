from argparse import ArgumentParser, Namespace

from chq.commands.parse_name import parse_chall_name
from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('name', type=str, help="name of the challenge")
    parser.add_argument("--only-init", dest="only_init", action="store_const", const=True, default=False, help="don't switch context after the initialization")
    parser.add_argument("--allow-exists", dest="allow_exists", action="store_const", const=True, default=False, help="don't stop the initialization even if the directory already exists")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())

    ctf_name, chall_name = parse_chall_name(res.name)
    if ctf_name is None:
        ctf_name = ctx["ctf"]
    assert chall_name is not None
    ctf_name, chall_name = normalize(ctf_name), normalize(chall_name)

    ctf = ctx.root.get_ctf(ctf_name)
    chall = ctf.get_chall(chall_name)
    chall.init(allow_exists=res.allow_exists)
    if not res.only_init:
        ctx.set_and_save("chall", chall_name)
    print(chall.path)

init_chall_command = SubCommand(
    "init-chall",
    _initializer,
    _handler,
    aliases=["init"],
    description="Initialize a challenge"
)
