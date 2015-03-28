#this file just opens a connection with the problem database
import MySQLdb
f=open('/home/ubuntu/passwd1.txt','r')
s=f.read()
f.close()
s=s.split('\n')
user=s[0]
passwd=s[1]
db=s[2]
db=MySQLdb.connect("localhost",user,passwd,db)
cursor=db.cursor()
