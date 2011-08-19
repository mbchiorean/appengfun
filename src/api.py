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
from datetime import datetime

from oauth_provider import oauth_request
from oauth_provider.decorators import oauth_required

from common import BaseHandler
from config import config

class OAuthSampleHandler(BaseHandler):
    @oauth_required
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('"Hello!"')

app = webapp2.WSGIApplication([
    ('/api/oauth_sample', OAuthSampleHandler),
    ('/api/request_token', oauth_request.RequestTokenHandler),
    ('/api/access_token', oauth_request.AccessTokenHandler),
    ('/api/authorize', oauth_request.AuthorizeHandler),
], debug=True, config=config)

def main():
    app.run()

if __name__ == '__main__':
    main()
