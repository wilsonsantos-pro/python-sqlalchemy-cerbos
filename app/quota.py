from pydantic import BaseModel


class Quota(BaseModel):
    contact_quota_limit: int = 10


def set_contact_quota_limit(limit: int) -> None:
    quota.contact_quota_limit = limit


quota = Quota()
