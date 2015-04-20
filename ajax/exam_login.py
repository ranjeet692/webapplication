#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Cache-Control:no-store, no-cache, must-revalidate"
print "Content-Type: text/html\n\n"

import cgi, cgitb,os, Cookie
from connection import cursor,db
from cookie import c,load_cookie

form = cgi.FieldStorage()
key = form.getvalue('key')
exam_id = form.getvalue('eid')
query="select * from exam where exam_id='{0}'".format(str(exam_id))
cursor.execute(query)
data=cursor.fetchone();
if(int(key) == int(data[6])):
	print str(1)
else:
	print str(0)
		
