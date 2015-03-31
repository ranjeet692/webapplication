#!/usr/bin/python
# -*- coding: utf-8 -*-
print "Content-Type: text/html\n\n"
from jinja2 import Template, Environment, FileSystemLoader
from connection import cursor, db
import cgi,cgitb,Cookie,os
import footer

data= cgi.FieldStorage()
course_id = data.getvalue('cid')
page = str(data.getvalue('page'))
#course_id = 1
user = ""
sql = "SELECT name,teacher_id FROM courses WHERE course_id = '{0}'".format(str(course_id))
cursor.execute(sql) 
data = cursor.fetchall()
f='/var/www/html/course/'+str(course_id)+'/syllabus.txt'
a=open(f)
desc=a.read()
a.close()
sql = "SELECT email_id, name, institute FROM teacher WHERE name = %s"
cursor.execute(sql,(data[0][1])) 
tdetails = cursor.fetchall()

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)
	user = c['name'].value
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
TEMPLATE_FILE = "/var/www/html/course_intro.html"
template = templateEnv.get_template( TEMPLATE_FILE )
if page == "index1.py":
	page = page + "#acourse"
templateVars = { "title" : data[0][0], "course_id": course_id, "prev_page": page, "footer":footer.html, "syllabus":desc,"tdetails":tdetails, "name": user}

print template.render(templateVars)
