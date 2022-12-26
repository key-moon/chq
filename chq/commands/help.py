from argparse import ArgumentParser, Namespace

from chq.commands.subcommand import SubCommand

def get_help_command(parser: ArgumentParser):
    def _initializer(parser: ArgumentParser):
        parser.add_argument('command', help='command name which help is shown')
        pass

    def _handler(res: Namespace):
        parser.parse_args([res.command, '--help'])

    return SubCommand(
        "help",
        _initializer,
        _handler,
        description="show help of the subcommand"
    )
