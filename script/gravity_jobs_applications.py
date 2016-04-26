from __future__ import unicode_literals
import base64
import json
import os
from urllib2 import Request, urlopen, HTTPError
from yattag import Doc, indent
from dateutil import parser
from post import Post

doc, tag, text = Doc().tagtext()
fetch_from = 0
fetch_size = 200
fetch_total = -1

# index_url = "http://staging-es4nonapp.vietnamworks.com/matchingInfo/_search?from={}&size={}"
# credentials = "staginges_readonly:Re@d0nly"
index_url = "http://es4nonapp.vietnamworks.com/matchingInfo/_search?from={}&size={}"
credentials = "productiones_readonly:Re@d0nly"

def write_job_application(job_applications, path):
  print ">> writing to file `job_applications.xml`";
  with open(path, "a") as f:
    for job_application in job_applications:
      with tag('jobApplication'):
        with tag('userId'):
          text(job_application["userId"])
        with tag('itemId'):
          text(job_application["itemId"])
        with tag('applyDate'):
          text(job_application["applyDate"])
      result = indent(doc.getvalue())
      f.write(result)
  f.close()


def write_header_tags(path):
  print ">>write header"
  f = open(path, "a")
  f.write("""
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:g="http://base.google.com/ns/1.0" xmlns:c="http://base.google.com/cns/1.0">
      <channel>
          <title>Vietnamworks uers</title>
          <link>http://www.vietnamworks.com/</link>
          <description>List of applications</description>
  """)
  f.close()


def write_footer_tags(path):
  print ">>write footer"
  f = open(path, "a")
  f.write("""
      </channel>
    </rss>
  """)
  f.close()


def gravity_user_apply(path, fetch_from, fetch_size, fetch_total):
  if os.path.exists(path):
    os.remove(path)

  write_header_tags(path)

  while True:
    print ">>fetching from: {}, size: {}".format(fetch_from, fetch_size)
    post = Post(index_url.format(fetch_from, fetch_size), credentials)
    payload = {
      "query": {
        "range": {
          "lastUpdateDate": {
            "gte": "now-1M"
          }
        }
      }
    }

    resp = post.make_request(payload)
    total = resp["hits"]["total"]
    print ">>es total: {}".format(total)
    if fetch_total == -1:
      fetch_total = total
    fetch_total = min(total, fetch_total)

    job_applications = []
    for i in range(0, len(resp[u'hits'][u'hits'])):
      source = resp[u'hits'][u'hits'][i][u'_source']
      if u'applyHistories' in source:
        for history in source[u'applyHistories']:
          job_applications.append({
            "userId": source["jobseekerId"],
            "itemId": history["jobId"],
            "applyDate": int(parser.parse(history["applyDate"]).strftime('%s'))
          })
      else:
        print "No applied history"

    write_job_application(job_applications, path)
    fetch_from = fetch_from + fetch_size
    if fetch_from > fetch_total:
      print ">>Stopping"
      break

  write_footer_tags(path)
  print ">>total: {}".format(fetch_from)


def main():
  gravity_user_apply("job_applications.xml", fetch_from, fetch_size, fetch_total)


if __name__ == '__main__':
  main()
