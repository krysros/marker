from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    )

from .meta import Base


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    fullname = Column(Unicode(50))
    position = Column(Unicode(50))
    phone = Column(Unicode(50))
    email = Column(Unicode(50))
