from typing import Any

from termcolor import colored
from dictum.cmd_builders.exec_info import ExecCmdInfo
from dictum.cmd_builders.nerdctl import get_nerdctl_cmd
from .selection.find_containers import find_container, find_deployments
from .cli import cli


def run(args: Any):
    c = find_container(args.selector)
    cmd = get_nerdctl_cmd(
        ExecCmdInfo(
            command=args.container_command,
            user=args.username,
            container_id=c,
        )
    )
    print(cmd)


def pause(args: Any):
    deps = find_deployments(args.selector)
    if not deps:
        print(colored("No deployments found", "red"))
        return
    for dep in deps:
        if dep.namespace == "kube-system":
            print(f"Skipping kube-system deployment {dep.metadata.name}")
            continue
        current_replicas = dep.spec.replicas
        paused_by_dictum = dep.labels.get("dictum/paused", "") == "true"
        if paused_by_dictum:
            print(f"Deployment {dep.metadata.name} already paused")
            continue
        current_replicas = dep.replicas
        dep.label(
            {
                "dictum/paused": "true",
                "dictum/old-replicas": str(current_replicas),
            }
        )
        dep.scale(0)

        print(f"Deployment {dep.metadata.name} paused")


def unpause(args: Any):
    deps = find_deployments(args.selector)
    if not deps:
        print(colored("No deployments found", "red"))
        return
    for dep in deps:
        if dep.namespace == "kube-system":
            print(f"Skipping kube-system deployment {dep.metadata.name}")
            continue
        current_replicas = dep.spec.replicas
        paused_by_dictum = dep.labels.get("dictum/paused", "") == "true"
        if not paused_by_dictum:
            continue
        if not dep.replicas == 0:
            print(
                f"Deployment {dep.metadata.name} has replicas, not unpausing. Scale it to 0 first"
            )
            continue

        old_replicas = int(dep.labels.get("dictum/old-replicas", "1"))
        dep.scale(old_replicas)
        dep.label(
            {
                "dictum/paused": "false",
                "dictum/old-replicas": "",
            }
        )

        print(f"Deployment {dep.metadata.name} unpaused")


def start():
    args = cli()
    match args.command:
        case "run":
            run(args)
        case "list":
            print("list")
        case "pause":
            pause(args)
        case "unpause":
            unpause(args)
        case _:
            print("unknown command")
            exit(1)
