from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from cerbos_example.database import Base

_INC = 1


def _get_str_inc():
    global _INC  # pylint: disable=global-statement
    s_inc = str(_INC)
    _INC = _INC + 1
    return s_inc


def reset_inc():
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
