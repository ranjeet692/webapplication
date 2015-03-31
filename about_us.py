#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi,cgitb,Cookie,os
from jinja2 import Template, Environment, FileSystemLoader 
print "Content-Type: text/html; charset=UTF-8\n\n"

templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )

user=""

if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)
	user = c['name'].value
	
TEMPLATE_FILE = "/var/www/html/about_us.html"	
templateVars = { "name": user}
template = templateEnv.get_template( TEMPLATE_FILE )
print template.render(templateVars)
