from typing import Generator
from ..init.kubernetes import k8s
import kr8s


def get_deployment_name_probably(pod_name: str):
    return "-".join(pod_name.split("-")[0:-2])


def find_deployments(selectors_line: list[str]) -> list[kr8s.objects.Deployment]:
    from dictum.selection.rephrase_selectors import rephrase_selectors

    api = kr8s.api()
    selectors = rephrase_selectors([*selectors_line])
    deps = kr8s.objects.Deployment.list(
        namespace=kr8s.ALL,
        field_selector=selectors.field_selector,
        label_selector=selectors.label_selector,
    )

    r = [*deps]
    return r


def find_container(selectors_line: list[str]) -> str:
    from dictum.selection.rephrase_selectors import rephrase_selectors

    selectors = rephrase_selectors([*selectors_line, "status.phase=Running"])
    results = k8s.list_pod_for_all_namespaces(
        label_selector=selectors.label_selector,
        field_selector=selectors.field_selector,
    )
    if len(results.items) == 0:
        raise ValueError(f"Selector {' '.join(selectors_line)} matched no pods")

    if len(results.items) > 1:
        raise ValueError(f"Selector {' '.join(selectors_line)} matched multiple pods")
    containers = [
        c_status.container_id.split("://")[1]
        for result_pod in results.items
        for c_status in result_pod.status.container_statuses
        if c_status.state.running
    ]
    if len(containers) == 0:
        raise ValueError(f"Pod {' '.join(selectors_line)} has no running containers")

    if len(containers) > 1:
        raise ValueError(
            f"Pod {' '.join(selectors_line)} has multiple running containers"
        )
    return containers[0]
