import datetime

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    Unicode,
    DateTime,
    Date,
    )

from sqlalchemy.orm import relationship

from slugify import slugify
from .meta import Base


investors_tenders = Table(
    'investors_tenders', Base.metadata,
    Column('investor_id', Integer,
           ForeignKey('investors.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('tender_id', Integer,
           ForeignKey('tenders.id', onupdate='CASCADE', ondelete='CASCADE'))
)


class Tender(Base):
    __tablename__ = 'tenders'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    city = Column(Unicode(100))
    link = Column(Unicode(2000))
    deadline = Column(Date)
    added = Column(DateTime, default=datetime.datetime.now)
    edited = Column(DateTime, default=datetime.datetime.now,
                    onupdate=datetime.datetime.now)
    submitter_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    editor_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    added_by = relationship('User', foreign_keys=[submitter_id])
    edited_by = relationship('User', foreign_keys=[editor_id])
    investor = relationship('Investor', secondary=investors_tenders,
                            backref='tenders', uselist=False)

    def __init__(self, name, city, investor, link, deadline):
        self.name = name
        self.city = city
        self.investor = investor
        self.link = link
        self.deadline = deadline

    @property
    def slug(self):
        return slugify(self.name)
