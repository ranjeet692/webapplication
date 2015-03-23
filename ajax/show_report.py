#!/usr/bin/python

print "Content-Type: text/html\n"

import cgi, cgitb
from connection import cursor, db
import problem_connect
data= cgi.FieldStorage()
aid= data.getvalue("aid")
pid = data.getvalue("pid")
f='/home/ubuntu/plagiarism/'+str(aid)+'/'+str(pid)+'/'+str(pid)+'.txt'
c=open(f,'r')
co=c.read()
c.close()
print '''<div class="modal-header">
        	<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>	
		<h4 class="modal-title" id="exampleModalLabel">Problem Id <span id='pid'>'''+str(pid)+'''</span></h4>
	 </div>
      	<div class="modal-body">
      		'''+str(co)+'''
      </div>
	<div class="modal-footer">      
	</div>'''

