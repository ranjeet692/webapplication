#!/usr/bin/python
# -*- coding: utf-8 -*-
from connection import cursor
import cgi,cgitb
import datetime
from cookie import c,load_cookie
form = cgi.FieldStorage()
eid=form.getvalue('eid')
query="select * from exam where exam_id='{0}'".format(str(eid))
cursor.execute(query)
data=cursor.fetchone()
load_cookie()
if(datetime.datetime.now()<data[5]):
	print "Cache-Control:no-store, no-cache, must-revalidate"
	print "Content-Type: text/html\n\n"
	print '1'
else:
	c["exam"]["expires"]='Thu, 01 Jan 1970 00:00:00 GMT'
	print c.output()
	print "Cache-Control:no-store, no-cache, must-revalidate"
	print "Content-Type: text/html\n\n"
	print '0'
