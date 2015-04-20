#!/usr/bin/python
print "Content-Type: text/html\n"

import cgi, cgitb
from connection import cursor, db

data= cgi.FieldStorage()

problem_id = data.getvalue("pid")

#print classid
#print field

sql = "SELECT testcase from testcase_submission WHERE problem_id = {0}".format(problem_id)
cursor.execute(sql)
data = cursor.fetchone()
if data is not None: 
    testcase = data[0]
else:
    testcase = "1"
    
print testcase
