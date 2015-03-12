#this file just opens a connection with the database
import MySQLdb
f=open('/home/ubuntu/passwd.txt','r')
s=f.read()
f.close()
s=s.split('\n')
user=s[0]
passwd=s[1]
db=s[2]
db=MySQLdb.connect("localhost","root","codemafia","neoscriptdb")
cursor=db.cursor()

