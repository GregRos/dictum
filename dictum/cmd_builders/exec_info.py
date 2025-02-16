from attr import dataclass


@dataclass
class ExecCmdInfo:
    command: str
    user: str
    container_id: str
