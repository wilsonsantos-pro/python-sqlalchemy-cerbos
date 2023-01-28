from cerbos.sdk.model import Principal, Resource
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select

from cerbos_example.auth import principal_from_username
from cerbos_example.database import Session

from .models import Contact

security = HTTPBasic()


# Stored users:
#   "alice": "admin",
#   "john": "user",
#   "sarah": "user",
#   "geri": "user",
def get_principal(credentials: HTTPBasicCredentials = Depends(security)) -> Principal:
    username = credentials.username

    principal = principal_from_username(username)
    if not principal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return principal


def get_db_contact(contact_id: str) -> Contact:
    with Session() as session:
        contact = session.scalars(
            select(Contact).where(Contact.id == contact_id)
        ).first()
        if contact is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found",
            )
    return contact


def get_resource_from_contact(
    db_contact: Contact = Depends(get_db_contact),
) -> Resource:
    return Resource(
        id=db_contact.id,
        kind="contact",
        attr=jsonable_encoder(
            {n.name: getattr(db_contact, n.name) for n in Contact.__table__.c}
        ),
    )
