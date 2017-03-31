from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    )

from slugify import slugify
from .meta import Base


class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50))

    def __init__(self, name):
        self.name = name

    @property
    def slug(self):
        return slugify(self.name)
