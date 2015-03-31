#!/usr/bin/python
print "Content-Type: text/html\n\n"
import c_compile,java_compile
import cgi, os,Cookie, sys, subprocess
import stat,timeit
from random import randint
from connection import cursor, db
try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    message = 'Error'

#-------------Session-----------------
if 'HTTP_COOKIE' in os.environ:
	cookie_string=os.environ.get('HTTP_COOKIE')
	c=Cookie.SimpleCookie()
	c.load(cookie_string)
#problem_id = '27'
#assignment_id = '22'
#student_id = 'ranjeetkumar692@gmail.com'
#language = 'java'
#file_name = 'FileTest.java'
#j_file_name = 'FileTest.java'
#service_request = 'test_case'
#c = '''import java.util.Scanner;
#			class FileTest
#			{
#  				public static void main(String[] args)
# 				{
#    				Scanner in = new Scanner(System.in);
#  				System.out.println("Yes");
#   				}    
#			};'''

	
#-------------variables---------------
form = cgi.FieldStorage()
problem_id = form.getvalue('pid')
assignment_id = form.getvalue('aid')
student_id = c["uid"].value
language = form.getvalue('l')
file_name = form.getvalue('filename')  #name of file which maybe previously uploaded, if it is not null then no need to create new file. if file_name and j_file_name is different then rename file_name to j_file_name
j_file_name = form.getvalue('jfile')   #taking java file name from user
service_request = form.getvalue('action')
content = form.getvalue('content')
if service_request == 'custom_execute':
	c_input = form.getvalue('cinput')

#print code
#------------coding tool----------------
class CodeHandler:
	def __init__(self):
		pass
		
	def create_file(self, location, language):
		try:
			file_name = str(randint(100,999))+language #random number generator to assign a file name
		except:
			pass	
		else:
			#print file_name	
			return file_name	
		
	def save_file(self, sid, location, content, filename, pid, aid, lang):
		try:
			#print 'save'
			if not os.path.exists(location):
				os.makedirs(location)
				os.chmod(location, 0755)
			fn = os.path.basename(filename)
			#print 'saved'	
			fi=open(location + fn, 'wb')
			fi.write(str(content))
			fi.close()
			
  			sql = "INSERT INTO save_code(student_id, assignment_id, problem_id, file_name, language) VALUES ('{0}', {1}, {2}, '{3}','{4}') ON DUPLICATE KEY UPDATE file_name = '{5}'".format(sid, aid, pid, filename, lang, filename)
  			cursor.execute(sql)
  			db.commit()
			status = "<script>var f = '"+str(filename)+"'; document.getElementById('filename').value = f.trim();</script><strong>Saved</strong>"
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise
		else:
			return status
			
	def compile_file(self, location, filename, language, out_location):
		try:
			if not os.path.exists(out_location):
				os.makedirs(out_location)
				os.chmod(out_location, 0755)
			fi=open(out_location + 'temp.txt','wb')
			subprocess.call(['chmod','777','-R','/home/ubuntu/temp/'])	
			if language == "java":
				result = subprocess.call(['javac', str(location+filename) ,'-d',out_location], stderr=fi)
			elif language == "c":
				result = subprocess.call(['gcc', str(location+filename) ,'-o',out_location+'output'],stderr=fi)	
			else:	
				result = "<strong>Error</strong>"
			fi.close()
			fi=open(out_location + 'temp.txt','r+')
			result = str(fi.read()).replace(location,'')
			fi.close()
					
			if result=="":
				result = "<strong>Compiled Successfully</strong>"
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise
		else:
			return result
			
	def execute_file(self, out_location, filename, language, custom_input):
		try:
			st = os.stat(out_location)	
			os.chmod(out_location,st.st_mode | stat.S_IWGRP | stat.S_IWOTH)
			curr_working_path=os.getcwd()
			rel_path=out_location
			os.chdir(rel_path)
			in_file = 'in.txt'
			out_file = 'out.txt'
			fin = open(in_file, 'wb')
			fin.write(custom_input)
			fin.close()
			fout = open(out_file, 'w+')
			fout.write('<pre>')
			fout.close()
			if language == "java":
				filename = filename.replace('.java','')
				setup='''import subprocess,os;fdr=open("'''+in_file+'''","r");fdw=open("'''+out_file+'''","w")'''
				stmt="subprocess.call(['timeout','15s','java','"+str(filename)+"' ],stdin=fdr,stdout=fdw)"
				output = timeit.timeit(stmt,setup,number=1)
				#fi = open(out_file, 'r+')
				#output = fi.read()
				#fi.close()
			else:
				setup='''import subprocess,os;fdr=open("'''+in_file+'''","r");fdw=open("'''+out_file+'''","a")'''
				stmt='''subprocess.call(['timeout','15s','./output'],stdin=fdr,stdout=fdw)'''				
				output = timeit.timeit(stmt,setup,number=1)
			fout = open(out_file, 'a')
			fout.write('</pre>')
			fout.close()	
			fi = open(out_file, 'r+')
			output = fi.read()
			fi.close()
				
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise
		else:
			return output
			
	def execute_testcase(self, sid, pid, aid, filename, language):
		try:
			output = 'Error'
			lan = []
			time = []
			if language == 'java':
				#print 'here'
				java_compile.check_code(pid,aid,filename)
				save_result="update submission_code set tc1='{0}',tc2='{1}',tc3='{2}',tc4='{3}',tc5='{4}' where assignment_id='{5}' and problem_id='{6}' and email_id='{7}'".format(str(java_compile.re[0]),str(java_compile.re[1]),str(java_compile.re[2]),str(java_compile.re[3]),str(java_compile.re[4]),str(aid),str(pid),str(sid))
				#print 'executed'
				r=0
				
				for i in range(5):
					if java_compile.re[i]==True:
						r=r+1
					lan.append(java_compile.re[i])
					time.append(java_compile.t[i])
					time[i]=str(time[i])[:7]
				if r!=0:
					r=(float(r)/5)*100
				score="update submission_code set score='{0}' where assignment_id='{1}' and problem_id='{2}' and email_id='{3}'".format(str(r),str(aid),str(pid),str(sid))	
				st=java_compile.sti
				tm=java_compile.tm
				
			else:
				c_compile.check_code(pid,aid,filename)
				save_result="update submission_code set tc1='{0}',tc2='{1}',tc3='{2}',tc4='{3}',tc5='{4}' where assignment_id='{5}' and problem_id='{6}' and email_id='{7}'".format(str(c_compile.re[0]),str(c_compile.re[1]),str(c_compile.re[2]),str(c_compile.re[3]),str(c_compile.re[4]),str(aid),str(pid),str(sid))
				#print 'executed'
				r=0
				
				for i in range(5):
					if c_compile.re[i]==True:
						r=r+1
					lan.append(c_compile.re[i])
					time.append(c_compile.t[i])
					time[i]=str(time[i])[:7]
				if r!=0:
					r=(float(r)/5)*100
				score="update submission_code set score='{0}' where assignment_id='{1}' and problem_id='{2}' and email_id='{3}'".format(str(r),str(aid),str(pid),str(sid))	
				st=c_compile.sti
				tm=c_compile.tm
				
			if tm == 1:
				cursor.execute(save_result)			
				cursor.execute(score)
				db.commit()
				output = '<div class="panel-heading">Test Cases</div><div class="panel-body"><table class="table"><tr><th>#</th><th>Time</th><th>Result</th></tr>'
				for i in range(5):
					output = output + '<tr><td>'+str(i+1)+'</td><td>'+str(time[i])+'</td><td>'+str(lan[i])+'</td></tr>'
				output = output + '<tr><td>Your Score for the problem is '+str(r)+'%</td><td></td><td></td><tr/></table></div>'
			else:
				output = '<div class="breadcrumb">'+st+'</div>'		
		except:
			print "Execution error:", sys.exc_info()[0]
			raise
		else:
			return output	
	
#-------------end of class---------------------

ext = {'java':'.java', 'Java':'.java','c':'.c', 'C': '.c','c++':'.cpp', 'C++':'.cpp'}
code = CodeHandler()		
lang = language
loc = '/home/ubuntu/submission/'+student_id+'/'+str(assignment_id)+'/'

o_loc = '/home/ubuntu/temp/'+student_id+'/'+str(assignment_id)+'/'+str(problem_id)+'/'

#---------rename file form file_name to j_file_name--------------------------	
if(language == 'java'):
	if((file_name == '' or file_name == None ) and (j_file_name != '' or j_file_name != None )):
		file_name = j_file_name + ext[lang]
	elif((file_name != '' or file_name != None ) and (j_file_name != '' or j_file_name != None )):
			if(file_name != j_file_name):
				file_name = j_file_name + ext[lang]	

#----------------new file service request ---------------------------	

if service_request == 'save':
	if file_name == '' or file_name == None:
		file_name = code.create_file(loc,ext[lang])
	status = code.save_file(student_id, loc, content, file_name, problem_id,assignment_id, language)
	head = '<div class="breadcrumb">'
	
if service_request == 'compile':
	if file_name == '' or file_name == None:
		file_name = code.create_file(loc,ext[lang])
	status = code.save_file(student_id, loc, content, file_name, problem_id,assignment_id, language)
	status = code.compile_file(loc, file_name ,language, o_loc)	
	head = '<div class="breadcrumb">'
	
if service_request == 'custom_execute':
	if file_name == '' or file_name == None:
		file_name = code.create_file(loc,ext[lang])
	status = code.save_file(student_id, loc, content, file_name, problem_id,assignment_id, language)
	status = code.compile_file(loc, file_name , language, o_loc)
	status = code.execute_file(o_loc, file_name , language, c_input)
	head = '&nbsp;<b>Output</b><br/><div class="breadcrumb">'
	
if service_request == 'test_case':
	if file_name == '' or file_name == None:
		file_name = code.create_file(loc,ext[lang])
	#------------------------submission entry in database ------------------------------	
	sql = "select * from submission_code where assignment_id = '{0}' and problem_id = '{1}' and email_id = '{2}'".format(str(assignment_id),str(problem_id), str(student_id))
	cursor.execute(sql)
	if(cursor.rowcount > 0):
		sql = "UPDATE submission_code SET time = now(),file_name='{3}' WHERE assignment_id = '{0}' and problem_id = '{1}' and email_id = '{2}'".format(str(assignment_id),str(problem_id), str(student_id),str(file_name))
	else:	
		sql = "INSERT INTO submission_code(assignment_id,problem_id, email_id,file_name) VALUES('{0}','{1}','{2}','{3}')".format(str(assignment_id),str(problem_id), str(student_id),str(file_name))
	cursor.execute(sql)
	db.commit()	
	#-----------------------saving coding------------------------------------------
	status = code.save_file(student_id, loc, content, file_name, problem_id,assignment_id, language)
	#print status
	#-----------------------compiling code----------------------------------------
	#status = code.compile_file(loc, file_name , language, o_loc)
	#print status
	#----------------------executing testcases-----------------------------------
	status = code.execute_testcase(student_id, problem_id,assignment_id, file_name, language)	
	head='<div>'

status = status.replace('/home/ubuntu/temp/'+str(student_id)+'/'+(assignment_id)+'/'+str(problem_id)+'/','')	
status = status.replace('/home/ubuntu/submission/'+str(student_id)+'/'+(assignment_id)+'/','')			
print head
print status	
print '</div>'
				
	
