#!/usr/bin/python
# -*- coding: utf-8 -*-
print "Cache-Control:no-store, no-cache, must-revalidate"
import cgi,cgitb,Cookie,os,connection, footer
from jinja2 import Template, Environment, FileSystemLoader 
print "Content-Type: text/html\n\n"
from mixpanel import Mixpanel
mp = Mixpanel("d4de82f1514bafcd4aea2120c5b1a5db")
cgitb.enable()
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
title = 'login'
mp.track('page viewed', 'landingPage');
if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)
	TEMPLATE_FILE = "/var/www/html/default.html"
	#check user type modified on 22nd Jan
	#IF YOU ARE SEEING THIS ERROR THEN PLEASE REMOVE ALL COOKIES FOR THIS PAGE AND TRY AGAIN.
	try:
		if (c['type'].value == "teacher"):
			sql = "SELECT course_id, name FROM courses WHERE teacher_id = '{0}'".format(str(c['uid'].value))
			connection.cursor.execute(sql)
			courses = connection.cursor.fetchall()
			mp.track(c['uid'].value,'teacher_login')
			TEMPLATE_FILE = "/var/www/html/teacher_home.html" 
			templateVars = { "title": "Course List","name" : c['name'].value, "courses": courses,"footer": footer.html}
			template = templateEnv.get_template( TEMPLATE_FILE )
			print template.render(templateVars)
		elif(c['type'].value == "student"):
			course="select email,a.course_id,b.name, c.institute from enrolled as a,courses as b, teacher as c where a.course_id=b.course_id and b.teacher_id = c.email_id and email=('{0}')".format(str(c['uid'].value))
			connection.cursor.execute(course)
			enrolled=connection.cursor.fetchall()
			mp.track(c['uid'].value,'student_login')
			acourse="select a.course_id, a.name, a.timeline, b.name, b.institute from courses as a, teacher as b where a.teacher_id = b.email_id"
			connection.cursor.execute(acourse)
			all_courses=connection.cursor.fetchall()	
			p_query="select pp.ppid,pc.title,pc.difficulty from practise_problem as pp,problem_code as pc where ppid not in (select ppid from practise_submission where email_id='{0}') and pp.pid=pc.problem_id".format(str(c['uid'].value))
			connection.cursor.execute(p_query)
			p_problem=connection.cursor.fetchall()	
			s_query="select pp.ppid,pc.title,score from problem_code as pc,practise_problem as pp,practise_submission as ps where pp.pid=pc.problem_id and ps.email_id='{0}' and ps.ppid=pp.ppid" .format(str(c['uid'].value))
			connection.cursor.execute(s_query)
			s_problem=connection.cursor.fetchall()	
			TEMPLATE_FILE = "/var/www/html/home.html" 
			templateVars = { "name" :c['name'].value,"enrolled":enrolled,"all_courses":all_courses,"footer":footer.html,"p_problem":p_problem,"s_problem":s_problem}
			template = templateEnv.get_template( TEMPLATE_FILE )
			print template.render(templateVars)
		else:
			sql= "select a.course_id, a.name, a.teacher_id,institute from courses as a,teacher as b where 	a.teacher_id=b.email_id and institute=(select institute from hod where email_id='{0}')".format(str(c['uid'].value))
			connection.cursor.execute(sql)
			courses = connection.cursor.fetchall()
			mp.track(c['uid'].value,'hod_login')
			TEMPLATE_FILE = "/var/www/html/hod_home.html" 
			templateVars = { "title": "Course List","name" : c['name'].value, "courses": courses,"footer": footer.html}
			template = templateEnv.get_template( TEMPLATE_FILE )
			print template.render(templateVars)
	except KeyError:
		TEMPLATE_FILE = "/var/www/html/default.html"
		templateVars = { "footer": footer.html, "title_log":title}
		template = templateEnv.get_template( TEMPLATE_FILE )
		print template.render(templateVars)		
else:
	TEMPLATE_FILE = "/var/www/html/default.html"
	templateVars = { "footer": footer.html, "title_log":title}
	template = templateEnv.get_template( TEMPLATE_FILE )
	print template.render(templateVars)
