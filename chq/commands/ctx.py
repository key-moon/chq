from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root
from chq.util.path_normalize import normalize

def _initializer(parser: ArgumentParser):
    parser.add_argument('key', type=str)
    parser.add_argument('value', type=str)

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())
    if res.key is None:
        for key in ctx.key_location:
            if key not in ctx: continue
            print(f'{key}={ctx[key]}')
        return
    if res.key not in ctx:
        raise KeyError(res.key)
    if res.value is None:
        print(f'{res.key}={ctx[res.key]}')
        return
    else:
        ctx.set_and_save(res.key, res.value)

ctx_command = SubCommand(
    "ctx",
    _initializer,
    _handler
)
