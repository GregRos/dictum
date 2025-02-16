from typing import Any
from dictum.cmd_builders.exec_info import ExecCmdInfo
from dictum.cmd_builders.nerdctl import get_nerdctl_cmd
from .selection.find_containers import find_container
from .cli import cli


def run(args: Any):
    c = find_container(args.selector)
    cmd = get_nerdctl_cmd(
        ExecCmdInfo(
            command=args.command,
            user=args.username,
            container_id=c,
        )
    )
    print(cmd)


def start():
    args = cli()
    match args.command:
        case "run":
            run(args)
        case "list":
            print("list")

        case _:
            print("unknown command")
            exit(1)
