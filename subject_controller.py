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
from sqlalchemy.orm.exc import NoResultFound
from elixir import metadata, setup_all
from jinja2 import Environment, FileSystemLoader
from subject_models import Subject, Phone, Email
from ConfigParser import SafeConfigParser

cfg = SafeConfigParser()
cfg.read('db.cfg')

metadata.bind = cfg.get('Database', 'uri')
setup_all()

class NewSubjectController(object):

    def __init__(self, app=None): # this way if running standalone, gets app, else doesn't need it
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)

        if req.method != 'POST':
            resp = HTTPBadRequest('This page can only be accesses via POST')
            return resp(environ, start_response)
        else:
            env = Environment(loader=FileSystemLoader('templates/'))
            template = env.get_template('foo.html')
            template = template.render() #TODO: fill in vars for render

            resp = Response()
            resp.content_type='application/xhtml+xml'
            resp.unicode_body = template
            return resp(environ, start_response)

class SubjectListController(object):

    def __init__(self, app=None): # this way if running standalone, gets app, else doesn't need it
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)

        # TODO: have a GET parameter to restrict what rows to fetch
        # and use Subject.query.filter_by if that param exists

        subs = Subject.query.all()
        subjects = [s.to_dict() for s in subs]

        env = Environment(loader=FileSystemLoader('templates/'))
        template = env.get_template('subject_list.html')
        template = template.render(subjects=subjects)

        resp = Response()
        resp.content_type='application/xhtml+xml'
        resp.unicode_body = template
        return resp(environ, start_response)

if __name__ == '__main__':
    import os
    from paste import httpserver, fileapp, urlmap

    app = urlmap.URLMap()
    app['/media'] = fileapp.DirectoryApp(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'media'))
    app['/tabletheme'] = fileapp.DirectoryApp(os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'tabletheme'))
    app['/list'] = SubjectListController(app)
    app['/new'] = NewSubjectController(app)
    httpserver.serve(app, host='127.0.0.1', port=8080)
