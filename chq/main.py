from argparse import ArgumentParser
from chq.commands.help import get_help_command

from chq.commands.root import root_command
from chq.commands.ctx import ctx_command
from chq.commands.switch import switch_command
from chq.commands.init_chall import init_chall_command
from chq.commands.init_ctf import init_ctf_command
from chq.commands.list_chall import list_chall_command
from chq.commands.list_ctf import list_ctf_command
from chq.commands.move_chall import move_chall_command
from chq.commands.add_content import add_content_command
from chq.commands.solved import solved_command

from chq.commands.subcommand import register_subcommands

def get_parser():
    parser = ArgumentParser(prog="chq" , description="Manage ctfs and challenges")
    help_command = get_help_command(parser)
    register_subcommands(
        parser,
        [
            help_command,
            root_command,
            ctx_command,
            switch_command,
            init_chall_command,
            init_ctf_command,
            list_chall_command,
            list_ctf_command,
            move_chall_command,
            add_content_command,
            solved_command,
        ]
    )
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
