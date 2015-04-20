#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi, cgitb,os, Cookie
from connection import cursor,db
from cookie import c,load_cookie
from jinja2 import Template, Environment, FileSystemLoader
cgitb.enable();
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
load_cookie()
if c['type'].value == "student":
	student_id = c["uid"].value
   	form = cgi.FieldStorage()
   	exam_id=form.getvalue('eid')
   	query="select * from exam where exam_id='{0}'".format(str(exam_id))
   	cursor.execute(query)
   	data=cursor.fetchone()
	c['exam']="true"
	c['exam']['expires']=3*60*60
	print c.output()
	print "Cache-Control:no-store, no-cache, must-revalidate"
	print "Content-Type: text/html\n\n"
	TEMPLATE_FILE = "/var/www/html/exam_home.html" 
	template = templateEnv.get_template( TEMPLATE_FILE )
	templateVars={"name":c["name"].value,"eid":exam_id}	
	print template.render( templateVars )
		
