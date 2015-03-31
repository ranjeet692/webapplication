#!/usr/bin/python
print "Content-Type: text/html\n\n"
import smtplib
def sendemail(to, subject, message ):
	try:
		f=open('/home/ubuntu/mailpasswd.txt','r')
		s=f.read()
		s=s.split('\n')
		user=s[0]
		passwd=s[1]
		header = 'To:'+ to +'\n'+'From:'+ user +'\n'+'Subject:' + subject + '\n'
		footer = '\n\n\nRegards\nTeam NeoScript'
		msg = header + '\n' + message + '\n' + footer
		smtpserver = smtplib.SMTP("smtp.gmail.com",587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo
		smtpserver.login(user,passwd)	
		smtpserver.sendmail(user,to,msg)
		smtpserver.close()	
	except:
			print "Unexpected error:", sys.exc_info()[0]
			raise
		else:
			return "ok"	

