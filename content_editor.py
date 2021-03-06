#!/usr/bin/python
# -*- coding: utf-8 -*-

print "Cache-Control:no-store, no-cache, must-revalidate"
print "Content-Type: text/html\n\n"
from jinja2 import Template, Environment, FileSystemLoader
import cgi, cgitb,os
data = cgi.FieldStorage()
filename = data.getvalue("edit")
cid = data.getvalue("cid")

content = ""
#content load from file
f = open("/var/www/html/course/"+str(cid) + "/" +str(filename) + ".txt", "r")
content = str(f.read())
f.close()
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
TEMPLATE_FILE = "/var/www/html/content_editor1.html"
template = templateEnv.get_template( TEMPLATE_FILE )
templateVars = { "content" :  content, "file": str(filename), "cid":cid }
print template.render( templateVars )

