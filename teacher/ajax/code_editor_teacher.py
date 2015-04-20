#!/usr/bin/python
print "Content-Type: text/html\n\n"
import cgi, cgitb
import os, Cookie	

assignment_id = -1
exam_id = -1
form = cgi.FieldStorage()
email_id = form.getvalue("email_id")
problem_id= form.getvalue("pid")
assignment_id=form.getvalue("aid")
exam_id = form.getvalue("eid")
filename  = form.getvalue("file")

if(int(exam_id) > 0):
	contents = open("/home/ubuntu/submission/"+ email_id + "/e" + str(exam_id) + "/" + filename).read()
else:
	contents = open("/home/ubuntu/submission/"+ email_id + "/" + str(assignment_id) + "/" + filename).read()
print contents
