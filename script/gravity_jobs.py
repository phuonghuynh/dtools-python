from __future__ import unicode_literals

import mysql.connector
import base64
import json
import os
from urllib2 import Request, urlopen, HTTPError
from yattag import Doc, indent
from dateutil import parser

# cnx = mysql.connector.connect(user='scott', password='tiger',
#                               host='127.0.0.1',
#                               database='employees')
# cnx.close()

dbconfig = {
  "database": "vnw_core",
  "host": "172.16.22.31",
  "user": "datasync",
  "password": "fDD3aHB-sLdfFF"
}

doc, tag, text = Doc().tagtext()
fetch_from = 0
fetch_size = 2
fetch_total = 100

pool = mysql.connector.connect(pool_name="mypool", pool_size=5, **dbconfig)

def select_jobs(fetch_from, fetch_size):
  cursor = pool.cursor()
  query = ("Select jobid, jobtitle from tbljob Limit {}, {}".format(fetch_from, fetch_size))
  cursor.execute(query)
  jobs = []
  for (job_id, jobtitle) in cursor:
    print "job_id: {}".format(job_id)
    jobs.append({
      "itemId": job_id,
      "hidden": "true",
      "title": jobtitle
    })
  cursor.close()
  pool.close()
  return jobs

def main():
  jobs = select_jobs(fetch_from, fetch_size)
  print jobs

if __name__ == '__main__':
    main()
