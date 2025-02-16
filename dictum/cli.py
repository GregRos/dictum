from argparse import ArgumentParser
from typing import Protocol

selector_help = """
Selectors are in the form {name}={value}. They can be comma or space separated.

The following are supported:

- pod={name} - Selects a pod by name
  p={name}
- [label]={name} - Selects a pod by label named 'label'
- deployment={name} - Selects a pod by deployment name
  d={name}
- namespace={name} - Selects a pod by namespace
  ns={name}
  @name               

Without a namespace selector, defaults to all namespaces.    
"""


class Args(Protocol):
    non_interactive: bool
    selector: str
    username: str
    command: str


def cli():
    arg_parser = ArgumentParser(prog="dictum", description="With great k8s power...")

    subparsers = arg_parser.add_subparsers(
        title="command", required=True, dest="command"
    )

    types = subparsers.add_parser("types", help="List defined resource types")

    list = subparsers.add_parser("list", help="list resources by query")
    list.add_argument(
        "selector", nargs="+", help="a multipart selector for the resources"
    )
    run = subparsers.add_parser(
        "run", help="Run a command on a container in a Kubernetes pod, interactively"
    )

    run.add_argument(
        "-N",
        "--non-interactive",
        help="Don't run the command interactively",
        dest="non_interactive",
        action="store_true",
    )
    run.add_argument(
        "-s",
        "--selector",
        nargs="+",
        help="The selector to use to select the container to run the command on",
        dest="selector",
        required=True,
    )

    run.add_argument(
        "-u",
        "--username",
        help="The username or uid to use to run the command",
        dest="username",
        default="root",
    )

    run.add_argument(
        "-C",
        "--container_command",
        dest="container_command",
        help="The command to run",
        required=True,
    )

    return arg_parser.parse_args()
