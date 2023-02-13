from app.utils.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, JSONType


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    contact_no = Column(Integer, unique=True, nullable=False)
    location = Column(JSONType, nullable=True)

    facilitator = relationship("Facilitator", back_populates="user")


class Facilitator(Base):
    __tablename__ = 'facilitators'

    username = Column(String, ForeignKey("users.username"), primary_key=True)

    user = relationship("User", back_populates="facilitator")