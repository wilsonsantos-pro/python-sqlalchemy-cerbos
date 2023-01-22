# pylint: disable=redefined-outer-name,unused-argument
from typing import TYPE_CHECKING, Any, Dict, List

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

Username = str
ContactDict = Dict[str, Any]


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
    username: str,
    expected_contacts_for: Dict[Username, List[ContactDict]],
):
    headers = {
        "accept": "application/json",
    }
    auth = (username, "")
    response = client.get("/contacts", headers=headers, auth=auth)
    assert response.status_code == 200, response.json()
    assert response.json() == expected_contacts_for[username]
