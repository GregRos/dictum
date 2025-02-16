from dictum.cmd_builders.exec_info import ExecCmdInfo


def get_nerdctl_cmd(info: ExecCmdInfo) -> str:
    return f"nerdctl exec --namespace k8s.io  -u {info.user} -it {info.container_id} {info.command}"
