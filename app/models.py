from app.utils.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, JSONType


class Users(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    contact_no = Column(Integer, unique=True, nullable=False)
    location = Column(JSONType, nullable=True)

    facilitator = relationship("Facilitators", back_populates="user")


class Facilitators(Base):
    __tablename__ = 'facilitators'

    username = Column(String, ForeignKey("users.username"), primary_key=True)

    user = relationship("Users", back_populates="facilitator")
    support_group = relationship("SupportGroups", back_populates="sg_facilitator")
    rehab_centre = relationship("RehabCentres", back_populates="rc_facilitator")


# class Entity(Base):
#     __tablename__ = 'entities'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     contact_email = Column(EmailType, nullable=False)
#     contact_no = Column(Integer, nullable=False)
#     location = Column(JSONType, nullable=False)
#     facilitator = Column(String, nullable=False)


class SupportGroups(Base):
    __tablename__ = 'supportgroups'

    # id = Column(None, ForeignKey("entities.id"), primary_key=True)
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_email = Column(EmailType, nullable=False)
    contact_no = Column(Integer, nullable=False)
    location = Column(JSONType, nullable=False)
    facilitator = Column(String, ForeignKey("facilitators.username"), nullable=False)

    sg_facilitator = relationship("Facilitators", back_populates="support_group")


class RehabCentres(Base):
    __tablename__ = 'rehabcentres'

    # id = Column(None, ForeignKey("entities.id"), primary_key=True)
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    contact_email = Column(EmailType, nullable=False)
    contact_no = Column(Integer, nullable=False)
    location = Column(JSONType, nullable=False)
    facilitator = Column(String, ForeignKey("facilitators.username"), nullable=False)

    rc_facilitator = relationship("Facilitators", back_populates="rehab_centre")