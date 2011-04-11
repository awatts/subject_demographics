#!/usr/bin/env python

#Author: Andrew Watts
#
#    Copyright 2009-2010 Andrew Watts and the University of Rochester
#    Brain and Cognitive Sciences Department
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License version 2.1 as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.
#    If not, see <http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html>.

from datetime import date
from ConfigParser import SafeConfigParser
from sqlalchemy import Column, Integer, String, Unicode, Text, Date, Enum, Boolean, ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["Subject", "Phone", "Email"]

Base = declarative_base()

def from_dict(self, values):
    """Merge in items in the values dict into our object if it's one
    of our columns"""
    # from http://blog.mitechie.com/2010/04/03/a-follow-up-more-dict-to-sqlalchemy-fun/

    for c in self.__table__.columns:
        if c.name in values:
            setattr(self, c.name, values[c.name])

Base.from_dict = from_dict

class MyMixin(object):

    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id =  Column(Integer, primary_key=True)

class Subject(Base, MyMixin):

    __tablename__ = 'subject'

    __table_args__ = (UniqueConstraint('firstname', 'lastname', name='name_constraint'), MyMixin.__table_args__)

    entrydate = Column(Date(default = date.today))
    lastname = Column(Unicode(64) )
    firstname = Column(Unicode(64))
    phone_id = Column(Integer, ForeignKey('phone.id'))
    phone = relationship('Phone', backref='subject')
    email_id = Column(Integer, ForeignKey('email.id'))
    email = relationship('Email', backref='subject')
    age = Column(Integer())
    sex = Column(Enum(u'Male', u'Female'))
    ethnicity = Column(Enum(u'Hispanic or Latino', u'Not Hispanic or Latino'))
    amerind = Column(Boolean, default=False) # Ameican Indian
    afram = Column(Boolean, default=False) # African Ameican or Black
    pacif = Column(Boolean, default=False) # Pacific Islander or Native Hawaiian
    asian = Column(Boolean, default=False) # Asian
    white = Column(Boolean, default=False) # White
    unknown = Column(Boolean, default=False) # Unknown race
    other_race = Column(Unicode(32)) # Any other race specified
    ur_student = Column(Boolean, default=False) # Current UR student?
    gradyear = Column(Integer()) # year they will graduate
    hearing_normal = Column(Boolean, default=True)
    hearing_problems = Column(Text())
    vision_normal = Column(Enum(u'Normal uncorrected', u'Corrected-to-normal with glasses', u'Corrected-to-normal with soft contacts', u'Corrected-to-normal with hard contacts',u'Other'))
    vision_other = Column(Text()) # if vision_normal is 'Other', then what?
    more_expts = Column(Boolean, default=False)

    def __repr__(self):
        return '<Subject: %s, %s>' % (self.lastname, self.firstname)

class Phone(Base, MyMixin):

    __tablename__ = 'phone'

    number = Column(Unicode(24))

    def __repr__(self):
        return '<Phone: %s>' % (self.number)

class Email(Base, MyMixin):

    __tablename__ = 'email'

    address = Column(Unicode(128))

    def __repr__(self):
        return '<Email: %s>' % (self.address)
