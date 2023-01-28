from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import PlanResourcesResponse, Principal, ResourceDesc


def get_query_plan(
    principal: Principal, resource: str, action: str
) -> PlanResourcesResponse:
    with CerbosClient(host="http://localhost:3592") as cerbos:
        resource_description = ResourceDesc(resource)

        plan = cerbos.plan_resources(action, principal, resource_description)
    return plan
