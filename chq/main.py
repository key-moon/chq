from argparse import ArgumentParser

from chq.commands.root import root_command
from chq.commands.ctx import ctx_command
from chq.commands.init_chall import init_chall_command
from chq.commands.init_ctf import init_ctf_command
from chq.commands.list_chall import list_chall_command
from chq.commands.list_ctf import list_ctf_command

from chq.commands.subcommand import register_subcommands

# chq 

# ワークフローイメージ
# chq init-ctf SECCON-CTF-2022
# chq ctx ctf SECCON-CTF-2022
# chq init babypwn
# chq ctx chall babypwn
# chq add -x babypwn.tar.gz
# chq add solve.py
# chq restore chall.cpp -O _chall.cpp -y

# chq 

# chq init 
# chq init-ctf 
# chq remove 
# chq remove-ctf 

# chq list 
# chq list-ctf 

# chq root
def main():
    parser = ArgumentParser(description="")
    register_subcommands(
        parser,
        [
            root_command,
            ctx_command,
            init_chall_command,
            init_ctf_command,
            list_chall_command,
            list_ctf_command,
        ]
    )
    args = parser.parse_args()
    args.handler(args)
