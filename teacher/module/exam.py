	#!/usr/bin/python
import cgi,cgitb,sys
sys.path.insert(0, '/var/www/html')
from connection import db, cursor
from random import randint
class Exam:
	def __init__(self):
		pass
	
	def create_exam(self, title, type_e, course_id, start_time, end_time):
		try:
			
			sql = "INSERT into exam(title, startdate, enddate, course_id, type, code) VALUES(%s, %s, %s, %s, %s, %s)"
			cursor.execute(sql,(str(title), str(start_time), str(end_time), str(course_id), str(type_e), str(randint(11122121,89879249))))
			db.commit()
		except:
			pass	
		else:
			return "created"
		
	def update_exam(self, exam_id, title, type_e, start_time, end_time):
		try:
			sql = "UPDATE exam SET title = %s, startdate = %s, enddate = %s, type = %s WHERE exam_id = %s"
			cursor.execute(sql,(str(title), str(start_time), str(end_time), str(type_e), str(exam_id)))
			db.commit()
		except:
			print "Unexpected error:", sys.exc_info()[0]
		else:
			return "updated"
	def delete_exam(self, exam_id):
		pass
		
	def change_exam_code(self, exam_id):
		try:
			code = randint(11122121,89879249)
			sql = "SELECT * FROM exam WHERE exam_id = %s"
			cursor.execute(sql ,(str(exam_id)))
			if(cursor.rowcount > 0):
				sql = "UPDATE exam SET code = %s WHERE exam_id = %s"
				cursor.execute(sql, (code, exam_id))
				db.commit() 
			sql = "SELECT code FROM exam WHERE exam_id = %s"
			cursor.execute(sql ,(str(exam_id)))
			data = cursor.fetchone()
			if data is not None: 
				code_db = int(data[0])
			else:
				code_db = 0
			
		except:
			print "Unexpected error:", sys.exc_info()[0]
		else:
			if(code_db == code):
				return code
			else:
				"Error"
			
	def list_exam(self, course_id):
		try:
			sql = "SELECT * FROM exam WHERE course_id = %d ORDER BY startdate DESC"
			cursor.execute(sql,int(course_id))
			examlist = cursor.fetchall()
			i = 0
			assign = []  # list
			now = datetime.datetime.now() #cuurent date time
			for row in examlist:
				if row[5] == "code":
					sql = "SELECT count(*) FROM exam_code WHERE exam_id = %d"
					cursor.execute(sql,int(row[0]))
					count = cursor.fetchall() #count variable contains number of problems in an assignment from table assignment_code
					if(row[3] > now):         #if assignment enddate is greater than today's date then enable edit button.
						d = ""
						color = "info"
					else:
						d = "disabled"	
						color = ""
					row = row + (count[0][0],i+1,d,color,)     #adding 3 element in currunt tuple i.e. number of problems, serial no, button disable option
					assign.append(row)    #append each tuple(single row of a table to a list which'll later convert to multidimensional tuple)
				else:	
					sql = "SELECT count(*) FROM exam_mcq WHERE exam_id = %d"
					cursor.execute(sql,int(row[0]))
					count = cursor.fetchall()
					if(row[3] > now):
						d = ""
						color = "info"
					else:
						d = "disabled"	
						color = ""
					row = row + (count[0][0],i+1,d,color,)
					assign.append(row)
				i = i + 1	
			assign = tuple(assign)	
		except:
			pass
		else:
			return assign
				
	def list_exam_login_code(self, course_id):
		try:
			sql = "SELECT exam_id, title, code FROM exam WHERE course_id = %s ORDER BY startdate DESC"
			cursor.execute(sql,str(course_id))
			examlist = cursor.fetchall()
		except:
			print "Unexpected error:", sys.exc_info()[0]
		else:
			return examlist
	def record_exist(self, exam_id):
		try:
			sql = "SELECT * FROM WHERE exam_id = %d"
			cursor.execute(sql ,(int(exam_id)))
		except:
			pass
		else:
			return cursor.rowcount
								
	def assign_problem(self, exam_id, student_id, problem_id):
		try:
			pass
		except:
			pass
		else:
			pass
					
		sql = "SELECT * FROM problem_allotment WHERE exam_id = %s and student_id = %s and problem_id = %s"
		cursor.execute(sql ,(str(exam_id), str(student_id), str(problem_id)))
		data = cursor.fetchall()
		if(cursor.rowcount <= 0):
			sql = "INSERT INTO problem_allotment(exam_id, student_id, problem_id) VALUES(%s, %s, %s)"
			cursor.execute(sql, (str(exam_id),str(student_id), str(problem_id)))
			db.commit()
			
		return "saved"
	def update_assign_problem(self, exam_id, student_id, problem_id):
		sql = "SELECT * FROM problem_allotment WHERE exam_id = %d and student_id = %s and problem_id = %d"
		cursor.execute(sql ,(int(exam_id), str(student_id), int(problem_id)))
		data = cursor.fetchall()
		if(data.rowcount > 0):
			sql = "UPDATE problem_allotment SET problem_id = %d WHERE exam_id = %d and student_id = %s and problem_id = %d"
			cursor.execute(sql, (int(exam_id),str(student_id), int(problem_id)))
			db.commit()
		
	def delete_assign_problem(self, exam_id, student_id, problem_id):
		sql = "SELECT * FROM problem_allotment WHERE exam_id = %d and student_id = %s and problem_id = %d"
		cursor.execute(sql ,(int(exam_id), str(student_id), int(problem_id)))
		data = cursor.fetchall()
		if(data.rowcount > 0):
			sql = "DELETE TABLE problem_allotment WHERE exam_id = %d and student_id = %s and problem_id = %d"
			cursor.execute(sql, (int(exam_id),str(student_id), int(problem_id)))
			db.commit()
		pass
		
	def code_submission(self, exam_id, student_id, tc):
		
		pass
		

