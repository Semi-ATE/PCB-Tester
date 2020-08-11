# -*- coding: utf-8 -*-
from main.Database.base import Base
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

roles_users = Table(
    'roles_users',
    Base.metadata,
    Column('user_id', Integer(), ForeignKey('user.id')),
    Column('role_id', Integer(), ForeignKey('permission.id'))
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    psk = Column(String)
    permission = relationship(
        'Permission',
        secondary=roles_users,
        backref=backref('user', lazy='dynamic')
    )


    def __init__(self, username, psk, permission):
        self.username = username
        self.psk = psk
        self.permission = permission

    def __str__(self):
        return "id: {}, username: {}, psk: {}, permission: {}".format(self.id, self.username, self.psk, self.permission)
