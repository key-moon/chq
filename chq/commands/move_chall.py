from argparse import ArgumentParser, Namespace

from chq.commands.parse_name import parse_chall_name, parse_dest_name
from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('chall_name', help="name of the challenge")
    parser.add_argument("dest_ctf", help="name of the destination")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    
    ctf_name, chall_name = parse_chall_name(res.chall_name)
    if ctf_name is None or chall_name is None:
        raise Exception("invalid chall name", res.chall_name)
    ctf_name, chall_name = normalize(ctf_name), normalize(chall_name)

    dest_ctf_name, dest_chall_name = parse_dest_name(res.dest_ctf)
    if dest_ctf_name is None:
        dest_ctf_name = normalize(ctf_name + "-solved")
    if dest_chall_name is None:
        dest_chall_name = chall_name

    ctf = ctx.root.get_ctf(ctf_name)
    dest_ctf = ctx.root.get_ctf(dest_ctf_name)
    chall = ctf.get_chall(chall_name)
    dest_path = dest_ctf.path / dest_chall_name

    ctf.ensure_initialized()
    chall.ensure_initialized()
    dest_ctf.ensure_initialized()
    if dest_path.exists():
        raise FileExistsError(dest_path)

    chall.path.rename(dest_path)

    if ctx["ctf"] == ctf_name and ctx["chall"] == chall_name:
        ctx.set_and_save("chall", None)
        ctx.set_and_save("ctf", None)
        
        ctx.set_and_save("ctf", dest_ctf_name)
        ctx.set_and_save("chall", dest_chall_name)
    print(dest_path)

move_chall_command = SubCommand(
    "move-chall",
    _initializer,
    _handler,
    aliases=["move", "mv"],
    description="Move the challenge"
)
