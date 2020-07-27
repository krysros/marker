import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Unicode,
    DateTime,
    )

from sqlalchemy.orm import relationship

from slugify import slugify
from .meta import Base


class Investor(Base):
    __tablename__ = 'investors'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    city = Column(Unicode(100))
    link = Column(Unicode(2000))
    added = Column(DateTime, default=datetime.datetime.now)
    edited = Column(DateTime, default=datetime.datetime.now,
                    onupdate=datetime.datetime.now)
    submitter_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    editor_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    added_by = relationship('User', foreign_keys=[submitter_id])
    edited_by = relationship('User', foreign_keys=[editor_id])

    def __init__(self, name, city, link):
        self.name = name
        self.city = city
        self.link = link

    @property
    def slug(self):
        return slugify(self.name)
