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

from subject_models import Subject, Phone, Email
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ConfigParser

cfg = ConfigParser.SafeConfigParser()
cfg.read('db.cfg')

engine_string = cfg.get('db', 'engine_string')

engine = create_engine(engine_string)
Session = sessionmaker(bind=engine)

session = Session()

Subject.metadata.create_all(engine)
Phone.metadata.create_all(engine)
Email.metadata.create_all(engine)

session.commit()
