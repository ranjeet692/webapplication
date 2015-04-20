#!/usr/bin/python
# -*- coding: utf-8 -*-
print "Content-Type: text/html\n\n"
from jinja2 import Template, Environment, FileSystemLoader
from connection import cursor, db
import cgi, cgitb,Cookie,os
import footer
#data = cgi.FieldStorage()
#cid = data.getvalue("cid")
#cid = 1
#title = "Java Programming"
if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)

#u="vipul2519@gmail.com"
#sql = "select distinct(title),score from practise_submission as s,problem_code as p where s.ppid=p.problem_id and email_id = '{0}'".format(str(c['uid'].value))
sql="select score,time from submission_code where email_id='vipul2519@gmail.com' union select score,time_stamp as time from practise_submission where email_id='vipul2519@gmail.com' order by time"
cursor.execute(sql)
data = cursor.fetchall()
i=0
tc=[]
sc=[]
if cursor.rowcount >10:
	for row in data:
		tc.append([i,row[0]])
		i=i+1
		st='''<script type="text/javascript">
		        var dat='''+str(tc)+'''
	        //var ticks='''+str(sc)+'''
	        var dataset = [{ label: "Performance Graph", data: dat, color: "green" }];
	         var options={
	         		series:{
	         			lines:{
	         				show: true,
	         				//barWidth:0.8
	         				}
	         		        }
	         		//xaxis:{
	         		//	ticks:ticks         			
	        		//	}
	         	};
	        $(document).ready(function () {
	            $.plot($("#flot-placeholder"),dataset,options	
	             );
	            //$("#flot-placeholder").UseTooltip();
	        });
	         </script>'''
else:
	st="<div class='alert alert-success' role='alert'>Coding Is Fun Have Probelms About how to Begin Don't Worry Go to our Practise section Problems and Start Solving Problems with easy tag</div>"
print st
