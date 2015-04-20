#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi,cgitb,Cookie,os
from jinja2 import Template, Environment, FileSystemLoader 
print "Content-Type: text/html; charset=UTF-8\n\n"

templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )

user=""

TEMPLATE_FILE = "/var/www/html/about_us.html"
template = templateEnv.get_template( TEMPLATE_FILE )
print template.render()
