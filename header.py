#!/usr/bin/python
# -*- coding: utf-8 -*-
from jinja2 import Template, Environment, FileSystemLoader
import cgi,cgitb,Cookie,os
print "Content-Type: text/html\n\n"
cgitb.enable()
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)
	TEMPLATE_FILE = "/var/www/html/header_user.html"
else:
	TEMPLATE_FILE = "/var/www/html/header_guest.html"	
