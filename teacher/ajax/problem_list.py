#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Cache-Control:no-store, no-cache, must-revalidate"
print "Content-Type: text/html\n\n"

import cgi, cgitb
from connection import cursor

data = cgi.FieldStorage()
exam_id = -1
assignment_id = -1
assignment_id = data.getvalue("aid")
exam_id = data.getvalue("eid")

options = ""

if(int(exam_id) > 0):
	sql = "SELECT problem_id FROM exam_code WHERE exam_id = {0}".format(int(exam_id))
else:
	sql = "SELECT problem_id FROM assignment_code WHERE assignment_id = {0}".format(int(assignment_id))
	
cursor.execute(sql)
data = cursor.fetchall()
print data
for row in data:
	sql = "SELECT title FROM problem_code WHERE problem_id = {0}".format(int(row[0]))
	cursor.execute(sql)
	data1 = cursor.fetchall()
	if(cursor.rowcount > 0):
		for row1 in data1:
			options = "<option value='"+str(row[0])+"'>"+str(row1[0])+"</option>" + options
	else:
		options = "<option>No Problem</option>"
print options
