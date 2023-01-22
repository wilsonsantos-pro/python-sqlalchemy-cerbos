from typing import Optional

from cerbos.sdk.model import Principal
from sqlalchemy import select

from app.models import Session, User


def get_principal(username: str) -> Optional[Principal]:

    with Session() as dbsession:
        # retrieve `user` from the DB to access the attributes
        user = dbsession.scalars(select(User).where(User.username == username)).first()
        if user is None:
            return None

    return Principal(user.id, roles={user.role}, attr={"department": user.department})
