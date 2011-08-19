'''
Created on Aug 18, 2011

@author: BogdanC
'''
from google.appengine.ext import db

class UserLocale(db.Model):
    user = db.UserProperty()
    locale = db.StringProperty()
    datelocale = db.StringProperty()
    dateformat = db.StringProperty()
    
    
class DateS(db.Model):
    dat = db.DateProperty()
