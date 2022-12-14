from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand
from chq.fs.root import get_default_root

def _initializer(parser: ArgumentParser):
    pass

def _handler(res: Namespace):
    root = get_default_root()
    print(root.path)

root_command = SubCommand(
    "root",
    _initializer,
    _handler,
    description="Show the current root of challenges"
)
