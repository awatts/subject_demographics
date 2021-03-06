#!/usr/bin/env python

#Author: Andrew Watts
#
#    Copyright 2010 Andrew Watts and the University of Rochester BCS Department
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
#

from webob import Request, Response
from webob.exc import HTTPBadRequest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from jinja2 import Environment, FileSystemLoader
from subject_models import Subject, Phone, Email
from ConfigParser import SafeConfigParser
from datetime import date
from dateutil import parser
import os.path

basepath = os.path.dirname(__file__)

cfg = SafeConfigParser()
cfg.read(os.path.join(basepath, 'db.cfg'))
engine_string = cfg.get('db', 'engine_string')

class NewSubjectController(object):

    def __init__(self, app=None): # this way if running standalone, gets app, else doesn't need it
        self.app = app

    def __call__(self, environ, start_response):
    
        # SQLAlchemy boilerplate code to connect to db and connect models to db objects
        engine = create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        session = Session()

        req = Request(environ)

        if req.method != 'POST':
            resp = HTTPBadRequest('This page can only be accesses via POST')
            return resp(environ, start_response)
        else:
            firstname = req.POST['firstname']
            lastname = req.POST['lastname']
            subj = Subject(firstname=firstname, lastname=lastname)

            to_add = {}
            for k in ('amerind', 'afram', 'pacif', 'asian', 'white',
                      'unknown', 'ur_student', 'hearing_normal', 'more_expts'):
                if req.POST.has_key(k):
                    to_add[k] = True

            for k in ('sex', 'ethnicity', 'other_race', 'gradyear',
                      'hearing_problems', 'vision_normal', 'vision_other'):
                if req.POST.has_key(k):
                    if req.POST[k] not in (None, '', u''):
                        to_add[k] = req.POST[k]

            if req.POST.has_key('age'):
                if req.POST['age'] not in (None, ''):
                    to_add['age'] = int(req.POST['age'])

            if req.POST['entrydate'] not in (None, '', u''):
                to_add['entrydate'] = parser.parse(req.POST['entrydate']).date()
            else:
                to_add['entrydate'] = date.today()

            subj.from_dict(to_add)
            try:
                session.add(subj)
                session.commit()
            except IntegrityError as e:
                resp = HTTPBadRequest(e)
                return resp(environ, start_response)

            if req.POST.has_key('phone'):
                if req.POST['phone'] not in (None, '', u''):
                    p = Phone(subject = subj, number = req.POST['phone'])
                    session.add(p)
                    session.commit()

            if req.POST.has_key('email'):
                if req.POST['email'] not in (None, '', u''):
                    em = Email(subject = subj, address = req.POST['email'])
                    session.add(em)
                    session.commit()

            from pprint import pformat
            #output = pformat(subj.to_dict(deep={'phone': {}, 'email': {}}))
            env = Environment(loader=FileSystemLoader(os.path.join(basepath,'templates')))
            template = env.get_template('subject_list.html')
            template = template.render(subjects = [subj.to_dict(deep={'phone': {}, 'email': {}}),])

            resp = Response()
            resp.content_type='text/html'
            resp.unicode_body = template
            #resp.content_type='text/plain'
            #resp.body = output
            return resp(environ, start_response)

class SubjectListController(object):

    def __init__(self, app=None): # this way if running standalone, gets app, else doesn't need it
        self.app = app

    def __call__(self, environ, start_response):

        # SQLAlchemy boilerplate code to connect to db and connect models to db objects
        engine = create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        session = Session()

        req = Request(environ)

        # TODO: Add more possible filters. Do something w/ tuple below
        filterkeys = ('stardate', 'enddate', 'age', 'sex')

        subs = session.query(Subject)
        if req.params.has_key('startdate') and req.params.has_key('enddate'):
            subs = subs.filter(Subject.entrydate < req.params['enddate'], Subject.entrydate > req.params['startdate'])
        elif req.params.has_key('startdate'):
            subs = subs.filter(Subject.entrydate > req.params['startdate'])
        elif req.params.has_key('enddate'):
            subs = subs.filter(Subject.entrydate < req.params['enddate'])

        subs = subs.order_by(Subject.lastname).all()
        count = len(subs)
        subjects = [s.to_dict(deep={'phone': {}, 'email': {}}) for s in subs]

        env = Environment(loader=FileSystemLoader(os.path.join(basepath,'templates')))
        template = env.get_template('subject_list.html')
        template = template.render(subjects=subjects, count = count)

        resp = Response()
        resp.content_type='text/html'
        resp.unicode_body = template
        return resp(environ, start_response)

class SummaryController(object):

    def __init__(self, app=None): # this way if running standalone, gets app, else doesn't need it
        self.app = app

    def __call__(self, environ, start_response):

        # SQLAlchemy boilerplate code to connect to db and connect models to db objects
        engine = create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        session = Session()

        req = Request(environ)

        #TODO: have GET parameters to restrict by entry year what rows to fetch

        summary = {}
        summary['full_count'] = session.query(Subject).filter(None).count()
        summary['male'] = session.query(Subject).filter(Subject.sex == u'Male').count()
        summary['female'] = session.query(Subject).filter(Subject.sex == u'Female').count()
        summary['amerind'] = session.query(Subject).filter(Subject.amerind == True).count()
        summary['afram'] = session.query(Subject).filter(Subject.afram == True).count()
        summary['pacif'] = session.query(Subject).filter(Subject.pacif == True).count()
        summary['asian'] = session.query(Subject).filter(Subject.asian == True).count()
        summary['white'] = session.query(Subject).filter(Subject.white == True).count()
        summary['unknown']  = session.query(Subject).filter(Subject.unknown == True).count()
        summary['hisp'] = session.query(Subject).filter(Subject.ethnicity == u'Hispanic or Latino').count()
        summary['nonhisp'] = session.query(Subject).filter(Subject.ethnicity == u'Not Hispanic or Latino').count()

        env = Environment(loader=FileSystemLoader(os.path.join(basepath,'templates')))
        template = env.get_template('subject_summary.html')
        template = template.render(summary=summary)

        resp = Response()
        resp.content_type='text/html'
        resp.unicode_body = template
        return resp(environ, start_response)

class AddSubjectController(object):
    def __init__(self, app=None): # this way if running standalone, gets app, else doesn't need it
        self.app = app

    def __call__(self, environ, start_response):
        env = Environment(loader=FileSystemLoader(os.path.join(basepath,'templates')))
        template = env.get_template('entryform.html')
        template = template.render()

        resp = Response()
        resp.content_type='text/html'
        resp.unicode_body = template
        return resp(environ, start_response)



#class SubjectCSVExport(object):
#    
#    def __init__(self, app=None): # this way if running standalone, gets app, else doesn't need it
#        self.app = app
#
#    def __call__(self, environ, start_response):
#
#        # SQLAlchemy boilerplate code to connect to db and connect models to db objects
#        engine = create_engine(engine_string)
#        Session = sessionmaker(bind=engine)
#        session = Session()
#
#        req = Request(environ)
#
#        # do something with DictWriter and a file content type
#
#        stup = [(s.lastname, s.firstname, "{0} {1}".format(s.firstname, s.lastname) ,s.entrydate.isoformat(), s.sex[0]) for s in subjects]
#        colnames = ('Last Name', 'First Name', 'Name','Date First Run', 'Gender')
#        [dict(zip(colnames, x)) for x in stup]
#
#        with open('subject_list.csv','w') as subl:
#            dw = DictWriter(subl, fieldnames = colnames)
#            dw.writerow(dict(zip(colnames, colnames)))
#            for row in sdic:
#                dw.writerow(row)

if __name__ == '__main__':
    import os
    from paste import httpserver, fileapp, urlmap

    app = urlmap.URLMap()
    app['/media'] = fileapp.DirectoryApp(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'media'))
    app['/tabletheme'] = fileapp.DirectoryApp(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'tabletheme'))
    app['/list'] = SubjectListController(app)
    app['/summary'] = SummaryController(app)
    app['/'] = SummaryController(app)
    app['/new'] = NewSubjectController(app)
    app['/add'] = AddSubjectController(app)
    httpserver.serve(app, host='127.0.0.1', port=8080)
