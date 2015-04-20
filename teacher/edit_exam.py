#!/usr/bin/python
# -*- coding: utf-8 -*-
#Description: This script has two parts, one for generate template to create a new exam, and 2nd is to edit an old exam based on query string.
#Query String Variables: cid(course_id), option(new or edit), if edit then, aid(assignment_id)
#Created on : April 18, 2015
#Last Modified: April 18, 2015
#Auhtor: Optimus Prime

print "Content-Type: text/html\n\n"

from jinja2 import Template, Environment, FileSystemLoader
import cgi,cgitb,Cookie, os
from connection import db, cursor
import footer
import datetime
cgitb.enable() 
data = cgi.FieldStorage()
course_id = data.getvalue('cid')
option = data.getvalue('option')

if option == "edit":
	exam_id = data.getvalue('eid')

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)

templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
TEMPLATE_FILE = "/var/www/html/teacher/edit_exam.html"
template = templateEnv.get_template( TEMPLATE_FILE )

#----checking user's credential to access this page-----
sql = "SELECT teacher_id FROM courses WHERE course_id = %s"
cursor.execute(sql, (course_id))
data = cursor.fetchone()
if data is not None: 
    teacher_id = data[0]
else:
    teacher_id = ""
#--------------------------------------------------------

if c['type'].value == "teacher" and (c['uid'].value == teacher_id or c['uid'].value == 'vipul@uohyd.ac.in'):
	if option == "new":
		submit_button_text = "Create"
		templateVars = { "cid":course_id,"name": c['name'].value, "footer": footer.html,"submit_text":submit_button_text, "eid": str(-1) }
		print template.render(templateVars)
	else:
		now = datetime.datetime.now()
		sql = "SELECT exam_id, title, startdate, enddate, course_id, type FROM exam WHERE exam_id = {0}".format(exam_id)
		cursor.execute(sql)
		data = cursor.fetchall()
		title = data[0][1]
		startdate = data[0][2]
		enddate = data[0][3]
		ptype = data[0][5]
		if enddate > now:
			d = ""
		else:
			d = "disabled"
				
		if ptype == "MCQ":
			sql = "SELECT problem_id FROM exam_mcq WHERE exam_id = {0}".format(exam_id)
			cursor.execute(sql)
			data = cursor.fetchall()
			i=0;
			pdata = ''
			for row in data:
				i = i+1
				sql = "SELECT * FROM problem_mcq WHERE problem_id={0}".format(row[0])
				cursor.execute(sql)
				data1 = cursor.fetchall()
				pdata = pdata + '<tr><td>'+str(i)+'</td><td>'+data1[0][1]+'<p><span class="badge">'+data1[0][8]+'</span>&nbsp;<span class="badge">'+data1[0][7]+'</span></p></td><td><button type="button"  id="'+str(row[0])+'" onclick="removeProblem(this.id)" class="btn btn-info btn-block" '+d+'>Remove</button></td></tr>' 
			cselect = ""
			mselect = "selected"
		else:
			sql = "SELECT problem_id FROM exam_code WHERE exam_id = {0}".format(exam_id)
			cursor.execute(sql)
			data = cursor.fetchall()
			i=0;
			pdata = ''
			for row in data:
				i = i+1
				sql = "SELECT * FROM problem_code WHERE problem_id={0}".format(row[0])
				cursor.execute(sql)
				data1 = cursor.fetchall()
				pdata = pdata + '<tr><td>'+str(i)+'</td><td>'+data1[0][6]+'<p><span class="badge">'+data1[0][5]+'</span>&nbsp;<span class="badge">'+data1[0][4]+'</span></p></td><td><button type="button" id="'+str(row[0])+'"   onclick="removeProblem(this.id)" class="btn btn-info btn-block"'+d+'>Remove</button></td></tr>' 
			cselect = "selected"	
			mselect = ""
		submit_button_text = "Update"
		
		table_start = '<div class="table-responsive"><table class="table table-bordered table-striped"><tbody><tr><th>#</th><th>Title</th><th>Operation</th></tr>'
		
		table_end = '</tbody></table><a href="add_problem.py?eid='+exam_id+'&cid='+course_id+'&option='+option+'" role="button" class="btn btn-primary btn-block " '+d+'>Add Problem</a></div>'
		templateVars = { "cid":course_id,"name": c['name'].value, "footer": footer.html,"submit_text":submit_button_text, "eid": exam_id,"ptitle": title, "sdate":startdate, "edate": enddate,"cselect":cselect,"mselect":mselect,"d":d,"table_head": table_start, "data": pdata, "table_end": table_end }
		print template.render(templateVars)	
else:
	TEMPLATE_FILE = "/var/www/html/redirect.html"
	template = templateEnv.get_template( TEMPLATE_FILE )
	print template.render()		
