#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import common
from datetime import datetime
from webapp2_extras import i18n
from webapp2_extras.i18n import I18n
from webapp2_extras.appengine.users import users
from babel import localedata, Locale
from common import BaseHandler
from config import config
from supportedlocales import SupportedLocales
from models import UserLocale, DateS


class HelloWorldHandler(BaseHandler):
    
    def get(self):
        
        user = users.get_current_user()
        usrlocale = UserLocale.gql("WHERE user = :u",u=user).get()
        dateformat = ''
        lastaddeddate = None
        qdat = DateS.gql('ORDER BY __key__ DESC').get()
        
        if qdat:
            lastaddeddate = qdat.dat
            
        if usrlocale == None:
            locale=self.browser_locale()
            i18n.get_i18n().set_locale(locale)
            datLoc = I18n(self.request)
            datLoc.set_locale(locale)
            jqdatelocale = locale.replace('_', '-')
            if locale == 'en_US':
                dateformat = 'MM/dd/yyyy'
        else:
            locale = usrlocale.locale
            datelocale = usrlocale.datelocale
            i18n.get_i18n().set_locale(locale)
            jqdatelocale = datelocale.replace('_', '-')
            datLoc = I18n(self.request)       
            datLoc.set_locale(datelocale)
            dateformat = usrlocale.dateformat
            if dateformat == '' and usrlocale.datelocale =='en':
                dateformat = 'MM/dd/yyyy'
            
        if jqdatelocale not in SupportedLocales.locales:
            jqdatelocale = None
            
        if dateformat == '' or dateformat == None:
            dateformat = 'short'
            jqdateformat = None
        elif locale == 'en_US':
            jqdateformat = common.isotojqformat(dateformat)
        else:
            jqdateformat = common.isotojqformat(usrlocale.dateformat)

        message = i18n.gettext('Hello, world!')
        context = {
                    'message': message,
                    'thetime': datLoc.format_datetime(
                                        datetime.now(),
                                        format=dateformat),
                    'locale':jqdatelocale,
                    'dateformat':jqdateformat,
                    'datefromdb':datLoc.format_date(
                                        lastaddeddate,
                                        format=dateformat)
                  }
        self.render_response('tplhello.html', **context)
        
        
class LocaleChangerPage(BaseHandler):
    
    def get(self):
        
        locals = localedata.list()
        ll = [ Locale(loc) for loc in locals if Locale(loc).display_name != None ]
        ll.sort(key=lambda x: x.english_name)
        user = users.get_current_user()
        usrlocale = UserLocale.gql("WHERE user = :u", u=user).get()
        if usrlocale:
            if usrlocale.dateformat != '' or usrlocale.dateformat != None:
                customdateformat = usrlocale.dateformat
        else:
            customdateformat = None

        context = {'locales':ll,
                   'customdateformat':customdateformat
                   }
        self.render_response('changelocale.html', **context)
        
        
class LocaleChanger(BaseHandler):
    
    def post(self):
        
        selected_language_locale = self.request.get('langLocale')
        selected_date_locale = self.request.get('dateLocale')
        date_format = self.request.get('dateFormat')
        user = users.get_current_user()
        usrlocale = UserLocale.gql("WHERE user = :u", u=user).get()
        if usrlocale == None:
            usrlocale = UserLocale(user=user,
                                   locale=selected_language_locale,
                                   datelocale=selected_date_locale,
                                   dateformat=date_format)
            usrlocale.put()
            self.redirect('/')

        usrlocale.user = user
        usrlocale.locale = selected_language_locale
        usrlocale.datelocale = selected_date_locale
        usrlocale.dateformat = date_format
        usrlocale.save()
        usrlocale.put()
        self.redirect('/')
        
        
class AddDateTime(BaseHandler):
    
    def post(self):
        dd = self.request.get('datepicker')
        usr = UserLocale.gql("WHERE user=:u",u=users.get_current_user()).get()
        if usr :
            i18n.get_i18n().set_locale(usr.locale)
            if usr.dateformat or usr.dateformat == '':
                thedate=i18n.parse_date(dd)
                da = DateS(dat=thedate)
            else:
                datef = usr.dateformat
                isoformat = common.isotopyformat(datef)
                thedate = datetime.strptime(dd, isoformat).date()
                da = DateS(dat=thedate)
        else:
            i18n.get_i18n().set_locale(self.browser_locale())
            thedate=i18n.parse_date(dd)
            da = DateS(dat=thedate)
            
        da.put()
        self.redirect('/')
        

# launcher
app = webapp2.WSGIApplication([
    ('/', HelloWorldHandler),
    ('/changelocale',LocaleChangerPage),
    ('/newlocale',LocaleChanger),
    ('/addtime',AddDateTime)
], debug=True, config=config)
    
def main():
    app.run()

if __name__ == '__main__':
    main()
