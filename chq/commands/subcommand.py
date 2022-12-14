from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Type, Generic, TypeVar

@dataclass
class SubCommand:
    name: str
    
    parser_initializer: Callable[[ArgumentParser], None]
    handler: Callable[[Namespace], None]

    aliases: Optional[List[str]] = None
    description: Optional[str] = None

def register_subcommands(parser: ArgumentParser, subcommands: List[SubCommand]):
    subparser = parser.add_subparsers()
    for command in subcommands:
        parser = subparser.add_parser(command.name, description=command.description)
        command.parser_initializer(parser)
        parser.set_defaults(handler=command.handler)
