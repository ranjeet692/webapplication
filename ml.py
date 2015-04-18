#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi,cgitb,connection
print "Content-Type: text/html\n\n"
import email_config
from jinja2 import Template, Environment, FileSystemLoader
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
#cgitb.enable()
form = cgi.FieldStorage() 
email = form.getvalue('email')
to = email
query="select * from user where email_id='{0}'".format(str(email))
connection.cursor.execute(query)
data=connection.cursor.fetchone()
if connection.cursor.rowcount > 0:
	subject = 'Subject:Forgot Password@NeoScript.in \n'
	message = 'Your Password is :: ' +str(data[1])
else:
	sql = "SELECT email_id,code FROM confirmation WHERE email_id = '{0}'".format(str(email))
	connection.cursor.execute(sql)
	if connection.cursor.rowcount > 0:
		data = connection.cursor.fetchone()
		header = 'Subject: Account Confirmation Pending | Forgot Password'
		message = 'Your account confirmation is still pending please first activate your account using this link \n http://www.neoscript.in/confirm_account.py?var='+str(data[0][1])+'&email='+to+'\nif you have forgot your password then use forgot password option after activating your account'
	else:
		header = 'Subject: Register a new account'
		msg = 'You are not registered in NeoScript. \nFollow this link to register :: http://www.neoscript.in/register.html'
status = email_config.sendemail(to,subject,message)
TEMPLATE_FILE = "/var/www/html/redirect.html" 
template = templateEnv.get_template( TEMPLATE_FILE )
print template.render( )
