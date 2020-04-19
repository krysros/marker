import datetime

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    Unicode,
    Numeric,
    UnicodeText,
    DateTime,
    )

from sqlalchemy.orm import (
    relationship,
    backref,
    )

from .meta import Base


offers_branches = Table(
    'offers_branches', Base.metadata,
    Column('offer_id', Integer,
           ForeignKey('offers.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('branch_id', Integer,
           ForeignKey('branches.id', onupdate='CASCADE', ondelete='CASCADE'))
)


offers_companies = Table(
    'offers_companies', Base.metadata,
    Column('offer_id', Integer,
           ForeignKey('offers.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('company_id', Integer,
           ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE'))
)


offers_tenders = Table(
    'offers_tenders', Base.metadata,
    Column('offer_id', Integer,
           ForeignKey('offers.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('tender_id', Integer,
           ForeignKey('tenders.id', onupdate='CASCADE', ondelete='CASCADE'))
)


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    category = Column(Unicode(20))
    unit = Column(Unicode(10))
    cost = Column(Numeric(precision=10, scale=2))
    currency = Column(Unicode(3))
    description = Column(UnicodeText)
    added = Column(DateTime, default=datetime.datetime.now)
    edited = Column(DateTime, default=datetime.datetime.now,
                    onupdate=datetime.datetime.now)
    submitter_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    editor_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    added_by = relationship('User', foreign_keys=[submitter_id])
    edited_by = relationship('User', foreign_keys=[editor_id])
    company = relationship('Company', secondary=offers_companies,
                           backref='offers', uselist=False)
    branch = relationship('Branch', secondary=offers_branches,
                          backref=backref('offers', lazy='dynamic'),
                          uselist=False)
    tender = relationship('Tender', secondary=offers_tenders,
                          backref='offers', uselist=False)

    def __init__(self, company, branch, tender, category, unit, cost, currency, description):
        self.company = company
        self.branch = branch
        self.tender = tender
        self.category = category
        self.unit = unit
        self.cost = cost
        self.currency = currency
        self.description = description
