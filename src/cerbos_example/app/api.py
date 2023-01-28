from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from cerbos_sqlalchemy import get_query
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import delete, select

from cerbos_example.app.models import Contact, User
from cerbos_example.app.quota import quota
from cerbos_example.app.schemas import ContactSchema
from cerbos_example.auth.auth import is_allowed
from cerbos_example.auth.query import get_query_plan
from cerbos_example.database import Session

app = FastAPI()
security = HTTPBasic()


# Stored users:
#   "alice": "admin",
#   "john": "user",
#   "sarah": "user",
#   "geri": "user",
def get_principal(credentials: HTTPBasicCredentials = Depends(security)) -> Principal:
    username = credentials.username

    with Session() as session:
        # retrieve `user` from the DB to access the attributes
        user = session.scalars(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    return Principal(
        user.id,
        roles={user.role},
        attr={"department": user.department, "contact_quota": 5},
    )


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


@app.get("/contacts")
def get_contacts(principal: Principal = Depends(get_principal)):
    plan = get_query_plan(principal, "contact", "read")

    query = get_query(
        plan,
        Contact,
        {
            "request.resource.attr.owner_id": User.id,
            "request.resource.attr.department": User.department,
            "request.resource.attr.is_active": Contact.is_active,
            "request.resource.attr.marketing_opt_in": Contact.marketing_opt_in,
        },
        [(User, Contact.owner_id == User.id)],
        # [(User.__table__, Contact.__table__.c.owner_id==User.__table__.c.id)],
    )

    # Optionally reduce the returned columns
    # (`with_only_columns` returns a new `select`)
    # NOTE: this is wise to do as standard, to avoid implicit joins generated by sqla
    # `relationship()` usage, if present
    query = query.with_only_columns(
        Contact.id,
        Contact.first_name,
        Contact.last_name,
        Contact.is_active,
        Contact.marketing_opt_in,
    )
    # print(query.compile(compile_kwargs={"literal_binds": True}))

    with Session() as session:
        rows = session.execute(query).fetchall()

    return rows


@app.get("/contacts/{contact_id}")
def get_contact(
    db_contact: Contact = Depends(get_db_contact),
    principal: Principal = Depends(get_principal),
):
    resource = get_resource_from_contact(db_contact)

    with CerbosClient(host="http://localhost:3592") as cerbos:
        if not cerbos.is_allowed("read", principal, resource):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
            )

    return db_contact


@app.post("/contacts/new")
def create_contact(
    contact_schema: ContactSchema, principal: Principal = Depends(get_principal)
):
    resource = Resource(
        id="new",
        kind="contact",
        attr={"contact_quota_limit": quota.contact_quota_limit},
    )

    if not is_allowed("create", principal, resource):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
        )

    db_contact = Contact(**contact_schema.dict())
    with Session() as session:
        session.add(db_contact)
        session.commit()
        session.refresh(db_contact)

    return {"result": "Created contact", "contact": db_contact}


@app.put("/contacts/{contact_id}")
def update_contact(
    contact_schema: ContactSchema,
    db_contact: Contact = Depends(get_db_contact),
    principal: Principal = Depends(get_principal),
    resource: Resource = Depends(get_resource_from_contact),
):

    with CerbosClient(host="http://localhost:3592") as cerbos:
        if not cerbos.is_allowed("update", principal, resource):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
            )

    for field, value in contact_schema:
        setattr(db_contact, field, value)

    with Session() as session:
        session.add(db_contact)
        session.commit()
        session.refresh(db_contact)

    return {"result": "Updated contact", "contact": db_contact}


@app.delete("/contacts/{contact_id}")
def delete_contact(
    resource: Resource = Depends(get_resource_from_contact),
    principal: Principal = Depends(get_principal),
):

    with CerbosClient(host="http://localhost:3592") as cerbos:
        if not cerbos.is_allowed("delete", principal, resource):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
            )

    with Session() as session:
        session.execute(delete(Contact).where(Contact.id == resource.id))
        session.commit()

    return {"result": f"Contact {resource.id} deleted"}
