# pylint: disable=redefined-outer-name,unused-argument
from typing import TYPE_CHECKING, Any, Dict, Generator, List

import pytest
from sqlalchemy import delete, update

from cerbos_example.app.models import Contact, Session
from cerbos_example.app.quota import set_contact_quota_limit
from cerbos_example.app.schemas import ContactSchema

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

Username = str
ContactDict = Dict[str, Any]


@pytest.fixture
def headers() -> Dict:
    return {
        "accept": "application/json",
    }


@pytest.fixture
def expected_contacts_for() -> Dict[Username, List[ContactDict]]:
    return {
        "geri": [
            {
                "id": "1",
                "first_name": "Nick",
                "last_name": "Smyth",
                "is_active": True,
                "marketing_opt_in": True,
            },
            {
                "id": "5",
                "first_name": "Aleks",
                "last_name": "Kozlov",
                "is_active": True,
                "marketing_opt_in": True,
            },
        ],
        "john": [
            {
                "id": "1",
                "first_name": "Nick",
                "last_name": "Smyth",
                "is_active": True,
                "marketing_opt_in": True,
            },
            {
                "id": "2",
                "first_name": "Simon",
                "last_name": "Jaff",
                "is_active": False,
                "marketing_opt_in": True,
            },
            {
                "id": "3",
                "first_name": "Mary",
                "last_name": "Jane",
                "is_active": True,
                "marketing_opt_in": False,
            },
            {
                "id": "5",
                "first_name": "Aleks",
                "last_name": "Kozlov",
                "is_active": True,
                "marketing_opt_in": True,
            },
        ],
    }


@pytest.mark.parametrize("username", ["john", "geri"])
def test_get_contacts(
    client: "TestClient",
    headers: Dict,
    username: str,
    expected_contacts_for: Dict[Username, List[ContactDict]],
):
    auth = (username, "")
    response = client.get("/contacts", headers=headers, auth=auth)
    assert response.status_code == 200, response.json()
    assert response.json() == expected_contacts_for[username]


@pytest.fixture
def new_contact() -> Generator:
    new_contact = ContactSchema(
        first_name="Charlie",
        last_name="Harper",
        owner_id="1",
        company_id="2",
        is_active=True,
        marketing_opt_in=False,
    )
    yield new_contact
    with Session() as dbsession:
        dbsession.execute(
            delete(Contact).where(
                Contact.first_name == new_contact.first_name,
                Contact.last_name == new_contact.last_name,
            )
        )
        dbsession.commit()


@pytest.mark.parametrize("username,expected", [("john", 200), ("geri", 403)])
def test_create_new_contact(
    client: "TestClient",
    headers: Dict,
    username: str,
    expected: int,
    new_contact: ContactSchema,
):
    auth = (username, "")
    response = client.post(
        "/contacts/new", headers=headers, auth=auth, json=new_contact.dict()
    )
    assert response.status_code == expected, response.json()


def test_create_new_contact_quota(
    client: "TestClient",
    headers: Dict,
    new_contact: ContactSchema,
):
    set_contact_quota_limit(5)
    username = "john"
    auth = (username, "")
    response = client.post(
        "/contacts/new", headers=headers, auth=auth, json=new_contact.dict()
    )
    assert response.status_code == 403, response.json()


@pytest.fixture
def update_contact() -> Generator:
    update_contact = ContactSchema(
        first_name="Nick",
        last_name="Smyth",
        marketing_opt_in=True,
        is_active=False,
        owner_id="1",
        company_id="1",
    )
    yield update_contact
    with Session() as dbsession:
        dbsession.execute(
            update(Contact)
            .where(
                Contact.first_name == update_contact.first_name,
                Contact.last_name == update_contact.last_name,
            )
            .values(is_active=True)
        )
        dbsession.commit()


def test_update_contact(
    client: "TestClient",
    headers: Dict,
    update_contact: ContactSchema,
):
    contact_id = 1
    username = "john"
    auth = (username, "")
    response = client.put(
        f"/contacts/{contact_id}",
        headers=headers,
        auth=auth,
        json=update_contact.dict(),
    )
    assert response.status_code == 200, response.json()
    assert not response.json()["contact"]["is_active"]
