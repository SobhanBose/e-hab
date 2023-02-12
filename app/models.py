from app.utils.database import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    contact_no = Column(Integer, unique=True, nullable=False)
    pic = Column(String, nullable=True)