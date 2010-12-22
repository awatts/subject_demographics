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

from elixir import *
from datetime import date
from ConfigParser import SafeConfigParser

__all__ = ["Subject", "Phone", "Email"]

cfg = SafeConfigParser()
cfg.read('db.cfg')

metadata.bind = cfg.get('Database', 'uri')

class Subject(Entity):
    entrydate = Field(Date(default = date.today))
    lastname = Field(Unicode(64), primary_key = True)
    firstname = Field(Unicode(64), primary_key = True)
    phone = OneToMany('Phone')
    email = OneToMany('Email')
    age = Field(Integer())
    sex = Field(Enum(u'Male', u'Female'))
    ethnicity = Field(Enum(u'Hispanic or Latino', u'Not Hispanic or Latino'))
    amerind = Field(Boolean, default=False) # Ameican Indian
    afram = Field(Boolean, default=False) # African Ameican or Black
    pacif = Field(Boolean, default=False) # Pacific Islander or Native Hawaiian
    asian = Field(Boolean, default=False) # Asian
    white = Field(Boolean, default=False) # White
    unknown = Field(Boolean, default=False) # Unknown race
    other_race = Field(Unicode(32)) # Any other race specified
    ur_student = Field(Boolean, default=False) # Current UR student?
    gradyear = Field(Integer()) # year they will graduate
    hearing_normal = Field(Boolean, default=True)
    hearing_problems = Field(Text())
    vision_normal = Field(Enum(u'Normal uncorrected', u'Corrected-to-normal with glasses', u'Corrected-to-normal with soft contacts', u'Corrected-to-normal with hard contacts',u'Other'))
    vision_other = Field(Text()) # if vision_normal is 'Other', then what?
    more_expts = Field(Boolean, default=False)

    def __repr__(self):
        return '<Subject: %s, %s>' % (self.lastname, self.firstname)

class Phone(Entity):
    subject = ManyToOne('Subject')
    number = Field(Unicode(24))

    def __repr__(self):
        return '<Phone: %s>' % (self.number)

class Email(Entity):
    subject = ManyToOne('Subject')
    address = Field(Unicode(128))

    def __repr__(self):
        return '<Email: %s>' % (self.address)
