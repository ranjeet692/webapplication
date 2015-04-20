#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi,cgitb,connection,Cookie,os
from jinja2 import Template, Environment, FileSystemLoader 
print "Content-Type: text/html\n\n"
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
from mixpanel import Mixpanel
mp = Mixpanel("d4de82f1514bafcd4aea2120c5b1a5db")
mp.track('page viewed', 'acourse w/0 login');
acourse="select * from courses"
connection.cursor.execute(acourse)
all_courses=connection.cursor.fetchall()

user=""	
TEMPLATE_FILE = "/var/www/html/acourse.html" 
templateVars = { "all_courses":all_courses, "name":user}
template = templateEnv.get_template( TEMPLATE_FILE )
print template.render(templateVars)
