#!/usr/bin/python
print "Content-Type: text/html\n\n"

import cgi
import cgitb
import Cookie
import os
import sys
import json
from connection import db, cursor
data = cgi.FieldStorage()
exam_id = data.getvalue('eid')
problem_id = data.getvalue('pid')
course_id = data.getvalue('cid')
json_data = data.getvalue('jsonString')

sys.path.insert(0, '/var/www/html/teacher/module/')
import exam

#student list reg no and email_id
sql = "SELECT a.rno, a.email_id from student as a, enrolled as b where a.email_id = b.email and b.course_id = {0}".format(course_id)
cursor.execute(sql)
data = cursor.fetchall()
regno_email_map = {x.upper():y for x,y in data}

status = ""

exam_object = exam.Exam()
spmlist = json.loads(json_data)
for regno in spmlist[2]:
	status = exam_object.assign_problem(spmlist[0], regno_email_map[regno], spmlist[1])

print status	
