from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite://"

Base = declarative_base()

# in-memory database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    # Use a static pool to persist state with an in memory instance of sqlite
    poolclass=StaticPool,
)


_INC = 1


def _get_str_inc():
    global _INC  # pylint: disable=global-statement
    s_inc = str(_INC)
    _INC = _INC + 1
    return s_inc


def _reset_inc():
    global _INC  # pylint: disable=global-statement
    _INC = 1


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=_get_str_inc)
    username = Column(String(255))
    email = Column(String(255))
    name = Column(String(255))
    contacts = relationship("Contact", back_populates="owner")
    role = Column(String(255))
    department = Column(String(255))


class Company(Base):
    __tablename__ = "company"

    id = Column(String, primary_key=True, default=_get_str_inc)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime)
    name = Column(String(255))
    website = Column(String(255))
    contacts = relationship("Contact", back_populates="company")


class Contact(Base):
    __tablename__ = "contact"

    id = Column(String, primary_key=True, default=_get_str_inc)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)
    first_name = Column(String(255))
    last_name = Column(String(255))
    owner_id = Column(String, ForeignKey("user.id"))
    owner = relationship("User", back_populates="contacts", lazy="joined")
    company_id = Column(String, ForeignKey("company.id"))
    company = relationship("Company", back_populates="contacts", lazy="joined")
    is_active = Column(Boolean, default=False)
    marketing_opt_in = Column(Boolean, default=False)


# generate tables from sqla metadata
Base.metadata.create_all(engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Populate with example data
with Session() as session:
    coca_cola = Company(name="Coca Cola")
    legal_co = Company(name="Legal Co")
    pepsi_co = Company(name="Pepsi Co")
    capri_sun = Company(name="Capri Sun")
    session.add_all([coca_cola, legal_co, pepsi_co, capri_sun])
    session.commit()
    _reset_inc()

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
    _reset_inc()

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
