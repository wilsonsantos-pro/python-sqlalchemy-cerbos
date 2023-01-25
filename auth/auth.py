from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource


def is_allowed(action: str, principal: Principal, resource: Resource) -> bool:
    with CerbosClient(host="http://localhost:3592") as cerbos:
        return cerbos.is_allowed(
            action,
            principal,
            resource,
        )
