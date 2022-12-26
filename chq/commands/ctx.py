from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand
from chq.ctx import CTX
from chq.fs.root import get_initialized_default_root

def _initializer(parser: ArgumentParser):
    parser.add_argument('key', nargs="?", type=str, help="key of the context")
    parser.add_argument('value', nargs="?", type=str, help="value to set")
    parser.add_argument('--available-keys', dest="show_keys", action="store_const", const=True, default=False, help="show keys")
    parser.add_argument('--hide-key', dest="show_key", action="store_const", const=False, default=True, help="hide key")

def _handler(res: Namespace):
    ctx = CTX.get(get_initialized_default_root())

    if res.show_keys:
        print(*ctx.known_key.keys())
        return

    if res.key is None:
        for key in ctx.known_key:
            if key not in ctx: continue
            print(f'{key}={ctx[key]}' if res.show_key else ctx[key])
        return
    if res.value is None:
        if res.key not in ctx:
            raise KeyError(res.key)
        print(f'{res.key}={ctx[res.key]}' if res.show_key else ctx[res.key])
        return
    else:
        ctx.set_and_save(res.key, res.value)

ctx_command = SubCommand(
    "ctx",
    _initializer,
    _handler,
    description="Get and set contexts"
)
