# -*- coding: utf-8 -*-
from main.Database.base import Base
from sqlalchemy import Column, String, Integer

class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "id: {}, name: {}".format(self.id, self.name)