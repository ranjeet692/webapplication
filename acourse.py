#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi,cgitb,connection,Cookie,os
from jinja2 import Template, Environment, FileSystemLoader 
print "Content-Type: text/html\n\n"
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
acourse="select * from courses"
connection.cursor.execute(acourse)
all_courses=connection.cursor.fetchall()

user=""

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)
	user = c['name'].value
	
TEMPLATE_FILE = "/var/www/html/acourse.html" 
templateVars = { "all_courses":all_courses, "name":user}
template = templateEnv.get_template( TEMPLATE_FILE )
print template.render(templateVars)
