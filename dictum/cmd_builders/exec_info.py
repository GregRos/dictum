from dataclasses import dataclass


@dataclass
class ExecCmdInfo:
    command: str
    user: str
    container_id: str
