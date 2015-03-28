#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Cache-Control:no-store, no-cache, must-revalidate"
print "Content-Type: text/html\n\n"

from jinja2 import Template, Environment, FileSystemLoader
from connection import cursor, db
import cgi, cgitb,Cookie,os
import footer
data = cgi.FieldStorage()
cid = data.getvalue("cid")
title = "NeoScript | Report"

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)

templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
if c['type'].value == "teacher":
	query="select a.assignment_id,a.problem_id,b.title,c.title,c.startdate from plagiarism as a,problem_code as b,assignment as c where a.problem_id=b.problem_id and a.assignment_id=c.assignment_id and c.course_id='{0}'".format(str(cid))
	cursor.execute(query)
	d=cursor.fetchall()
	contents='''<br>
			<div class="panel panel-default">
			  <!-- Default panel contents -->
			  <div class="panel-heading">Plagiarism</div>
			  <div class="panel-body">
			 <!-- Table -->
  				<table class="table">
  			 <tr><th>Assignment Title</th><th>Problem Title</th><th>Date</th><th>View Report</th></tr>'''
  	for row in d:
  		contents=contents+'''<tr><td>'''+str(row[3])+'''</td><td>'''+str(row[2])+'''</td><td>'''+str(row[4])+'''</td><td><button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal" data-aid="'''+str(row[0])+'''" data-pid="'''+str(row[1])+'''">View Report</button></td></tr>'''
  	contents=contents+'''</table>
			</div>
			</div>'''
#	contents = open("../course/"+ str(cid) + "/report.txt").read()
	TEMPLATE_FILE = "/var/www/html/teacher/report.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	templateVars = { "title" : title,  "cid":cid,"name":c['name'].value,"content":contents ,"footer": footer.html }
	print template.render( templateVars )
else:
	TEMPLATE_FILE = "/var/www/html/redirect.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	print template.render(  )
