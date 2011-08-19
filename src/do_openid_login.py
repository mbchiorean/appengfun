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
import os
import webapp2
from datetime import datetime

from google.appengine.api import users

from webapp2_extras import i18n
from webapp2_extras import jinja2

from common import BaseHandler
from common import attrdict
from config import config

OPENID_PROVIDERS = (
    'Google.com/accounts/o8/id', # shorter alternative: "Gmail.com"
    'Yahoo.com',
    'MySpace.com',
    'AOL.com',
    'MyOpenID.com',
)

class OpenIDLoginHandler(BaseHandler):
    def get(self):
        providers = \
            [attrdict(name=s.split('.')[0],
                      url=users.create_login_url(self.request.get('continue'),
                                                 federated_identity=s.lower()))
             for s in OPENID_PROVIDERS]
        self.render_response('login.html', providers=providers)

app = webapp2.WSGIApplication([
    ('/_ah/login_required', OpenIDLoginHandler),
], debug=True, config=config)

def main():
    app.run()

if __name__ == '__main__':
    main()
