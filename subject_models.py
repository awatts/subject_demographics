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
from sqlalchemy.orm import relationship, ColumnProperty
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

def to_dict(self, deep = {}, exclude = []):
    """
    Output values of a row as a dictionary
    """
    # based partly on code from http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    # and mostly on http://elixir.ematia.de/trac/browser/elixir/trunk/elixir/entity.py
    col_prop_names = [p.key for p in self.__mapper__.iterate_properties	\
            if isinstance(p, ColumnProperty)]

    data = dict([(name, getattr(self, name)) \
            for name in col_prop_names if name not in exclude])

    for rname, rdeep in deep.iteritems():
        dbdata = getattr(self, rname)
        fks = self.__mapper__.get_property(rname).remote_side
        exclude = [c.name for c in fks]
        if dbdata is None:
            data[rname] = None
        elif isinstance(dbdata, list):
            data[rname] = [o.to_dict(rdeep, exclude) for o in dbdata]
        else:
            data[rname] = dbdata.to_dict(rdeep, exclude)
    return data

Base.to_dict = to_dict

class MyMixin(object):

    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id =  Column(Integer, primary_key=True)

class Subject(Base, MyMixin):

    __tablename__ = 'subject'

    __table_args__ = (UniqueConstraint('firstname', 'lastname', name='name_constraint'), MyMixin.__table_args__)

    entrydate = Column(Date(default = date.today))
    lastname = Column(Unicode(64) )
    firstname = Column(Unicode(64))
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
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship('Subject', backref='phone')

    def __repr__(self):
        return '<Phone: %s>' % (self.number)

class Email(Base, MyMixin):

    __tablename__ = 'email'

    address = Column(Unicode(128))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship('Subject', backref='email')

    def __repr__(self):
        return '<Email: %s>' % (self.address)
