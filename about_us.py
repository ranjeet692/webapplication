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

TEMPLATE_FILE = "/var/www/html/about_us.html"
template = templateEnv.get_template( TEMPLATE_FILE )
print template.render()
