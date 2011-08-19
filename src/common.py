#!/usr/bin/env python

import webapp2

from webapp2_extras import jinja2

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)
    def browser_locale(self):
        return self.request.headers['Accept-Language'].split(",")[0].replace('-','_')

class attrdict(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

def isotopyformat(date):
    ''' trasformes a iso date representation to py strpdate dateformat for
    parsing
    '''
    
    transf = date.replace('dd','%d').replace('MM','%m').replace('yyyy','%Y')
    return transf

def isotojqformat(date):
    '''iso date format to jquery date format '''
    
    transf = date.lower().replace('yyyy','yy')
    return transf