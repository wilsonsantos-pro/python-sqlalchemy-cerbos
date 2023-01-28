from cerbos_example.app.models import Company, Contact, User, reset_inc
from cerbos_example.database import Session


def example_data():
    """Populate with example data."""
    with Session() as session:
        coca_cola = Company(name="Coca Cola")
        legal_co = Company(name="Legal Co")
        pepsi_co = Company(name="Pepsi Co")
        capri_sun = Company(name="Capri Sun")
        session.add_all([coca_cola, legal_co, pepsi_co, capri_sun])
        session.commit()
        reset_inc()

        alice = User(
            name="Alice",
            username="alice",
            email="alice@cerbos.demo",
            role="admin",
            department="IT",
        )
        john = User(
            name="John",
            username="john",
            email="john@cerbos.demo",
            role="user",
            department="Sales",
        )
        sarah = User(
            name="Sarah",
            username="sarah",
            email="sarah@cerbos.demo",
            role="user",
            department="Sales",
        )
        geri = User(
            name="Geri",
            username="geri",
            email="geri@cerbos.demo",
            role="user",
            department="Marketing",
        )
        session.add_all([alice, john, sarah, geri])
        session.commit()
        reset_inc()

        session.add_all(
            [
                Contact(
                    first_name="Nick",
                    last_name="Smyth",
                    marketing_opt_in=True,
                    is_active=True,
                    owner=john,
                    company=coca_cola,
                ),
                Contact(
                    first_name="Simon",
                    last_name="Jaff",
                    marketing_opt_in=True,
                    is_active=False,
                    owner=john,
                    company=legal_co,
                ),
                Contact(
                    first_name="Mary",
                    last_name="Jane",
                    marketing_opt_in=False,
                    is_active=True,
                    owner=sarah,
                    company=pepsi_co,
                ),
                Contact(
                    first_name="Christina",
                    last_name="Baker",
                    marketing_opt_in=True,
                    is_active=False,
                    owner=sarah,
                    company=capri_sun,
                ),
                Contact(
                    first_name="Aleks",
                    last_name="Kozlov",
                    marketing_opt_in=True,
                    is_active=True,
                    owner=sarah,
                    company=pepsi_co,
                ),
            ],
        )
        session.commit()
