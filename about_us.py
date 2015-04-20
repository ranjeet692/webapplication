#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi,cgitb,Cookie,os
from jinja2 import Template, Environment, FileSystemLoader 
print "Content-Type: text/html; charset=UTF-8\n\n"
from mixpanel import Mixpanel
mp = Mixpanel("d4de82f1514bafcd4aea2120c5b1a5db")
mp.track('page viewed', 'about_us');
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
