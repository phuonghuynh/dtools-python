from __future__ import unicode_literals

import base64
import json
import os
from urllib2 import Request, urlopen, HTTPError
from yattag import Doc, indent
from dateutil import parser

doc, tag, text = Doc().tagtext()
fetch_from = 0
fetch_size = 20
fetch_total = 100


# server_url = options.server_url
# credentials = options.credentials
# credentials = base64.encodestring('%s' % credentials).replace('\n', '')

class Post:
  def __init__(self, endpoint, credentials):
    self.endpoint = endpoint
    self.credentials = base64.encodestring('%s' % credentials).replace('\n', '')

  def post(self, payload):
    try:
      headers = {
        # 'Content-Type': 'application/vnd.json+api',
        'Authorization': 'Basic ' + self.credentials
      }
      request = Request(self.endpoint, data=payload, headers=headers)
      return json.loads(urlopen(request).read())
    except HTTPError as error:
      print payload
      print json.loads(error.read())
      raise error

  def make_request(self, payload):
    values = json.dumps(payload)
    print ">>posting to " + self.endpoint
    response = self.post(values)
    # print response
    return response


