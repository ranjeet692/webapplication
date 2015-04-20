#!/usr/bin/python
# -*- coding: utf-8 -*-
print "Cache-Control:no-store, no-cache, must-revalidate"
import cgi,cgitb,Cookie,sha,time,os
import connection
import footer
from mixpanel import Mixpanel
#import session
from jinja2 import Template, Environment, FileSystemLoader
#for error reporting
cgitb.enable()
mp = Mixpanel("d4de82f1514bafcd4aea2120c5b1a5db")
mp.track('page viewed', 'landingPage');
#what is the use of this line
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
# Create instance of FieldStorage 
form = cgi.FieldStorage() 
email = form.getvalue('email')
password  = form.getvalue('password')
login="select * from user where email_id = %s and password = %s"
connection.cursor.execute(login,(email,password))
data=connection.cursor.fetchall()
reg=False
if(connection.cursor.rowcount == 1):
		reg=True
		name=data[0][3]
		type=data[0][2]
		
if(reg==False):
	print "Content-Type: text/html\n\n"
	message="Wrong Details"
	TEMPLATE_FILE = "/var/www/html/default.html" 
	template = templateEnv.get_template( TEMPLATE_FILE )
	templateVars={"message":message}	
	print template.render( templateVars )

if(reg==True):	
	cookie = Cookie.SimpleCookie()
   	cookie['name'] = name
   	cookie['name']['expires'] = 12 * 30 * 24 * 60 * 60
	cookie['uid']=email
	cookie['uid']['expires'] = 12 * 30 * 24 * 60 * 60	
	#set cookie for login type
	cookie['type'] = type
	cookie['type']['expires'] = 12 * 30 * 24 * 60 * 60
	#modified on 22 jan
	print cookie.output()
	print "Content-Type: text/html\n\n"
	#if user is a teacher 
	#IF YOU ARE SEEING THIS ERROR THEN PLEASE REMOVE ALL COOKIES FOR THIS PAGE AND TRY AGAIN.
	if(type == "teacher"):
		sql = "SELECT course_id, name FROM courses WHERE teacher_id = '{0}'".format(str(email))
		connection.cursor.execute(sql)
		courses = connection.cursor.fetchall()
		TEMPLATE_FILE = "/var/www/html/teacher_home.html" 
		templateVars = { "title": "Course List","name" : cookie['name'].value, "courses": courses,"footer": footer.html}
		template = templateEnv.get_template( TEMPLATE_FILE )
		print template.render(templateVars)
	elif(type == "student"):	
		course="select email,a.course_id,b.name, c.institute from enrolled as a,courses as b, teacher as c where a.course_id=b.course_id and b.teacher_id = c.email_id and email='{0}'".format(str(email))
		connection.cursor.execute(course)
		enrolled=connection.cursor.fetchall()
		acourse="select a.course_id, a.name, a.timeline, b.name, b.institute from courses as a, teacher as b where a.teacher_id = b.email_id"
		connection.cursor.execute(acourse)
		all_courses=connection.cursor.fetchall()
		p_query="select pp.ppid,pc.title,pc.difficulty from practise_problem as pp,problem_code as pc where ppid not in (select ppid from practise_submission where email_id='{0}') and pp.pid=pc.problem_id".format(str(email))
		s_query="select pp.ppid,pc.title,score from problem_code as pc,practise_problem as pp,practise_submission as ps where pp.pid=pc.problem_id and ps.email_id='{0}' and ps.ppid=pp.ppid".format(str(email))
		connection.cursor.execute(p_query)
		p_problem=connection.cursor.fetchall()
		connection.cursor.execute(s_query)
		s_problem=connection.cursor.fetchall()		
		TEMPLATE_FILE = "/var/www/html/home.html" 
		template = templateEnv.get_template( TEMPLATE_FILE )
		templateVars = { "name" : name, "enrolled":enrolled,"all_courses":all_courses, "footer": footer.html,"p_problem":p_problem,"s_problem":s_problem}
		print template.render( templateVars )
	else:
		sql= "select a.course_id, a.name, a.teacher_id,institute from courses as a,teacher as b where a.teacher_id=b.email_id and institute=(select institute from hod where email_id='{0}')".format(str(email))
                connection.cursor.execute(sql)
		courses = connection.cursor.fetchall()
		TEMPLATE_FILE = "/var/www/html/hod_home.html" 
		templateVars = { "title": "Course List","name" : cookie['name'].value, "courses": courses,"footer": footer.html}
		template = templateEnv.get_template( TEMPLATE_FILE )
		print template.render(templateVars)

