from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    Unicode,
    )

from sqlalchemy.orm import relationship

from .meta import Base
from passlib.apps import custom_app_context as pwd_context


upvotes = Table(
    'upvotes', Base.metadata,
    Column('company_id', Integer,
           ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('user_id', Integer,
           ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
)


marker = Table(
    'marker', Base.metadata,
    Column('company_id', Integer,
           ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('user_id', Integer,
           ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(30), unique=True)
    fullname = Column(Unicode(50))
    email = Column(Unicode(50))
    role = Column(Unicode(20))
    _password = Column('password', Unicode(255))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pw):
        self._password = pwd_context.encrypt(pw)

    def check_password(self, pw):
        return pwd_context.verify(pw, self._password)

    upvotes = relationship('Company',
                           secondary=upvotes,
                           backref='companies')

    marker = relationship('Company',
                          secondary=marker,
                          backref='marker_companies')
