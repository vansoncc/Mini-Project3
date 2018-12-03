import pymysql
import datetime




##---------------Create Database---------------##
def Create_base():
    db = pymysql.connect(host='localhost',user='root', password='', port=3306)
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    data = cursor.fetchone()
    print('Database version:', data)
    cursor.execute("CREATE DATABASE IF NOT EXISTS  Mini_Project3 DEFAULT CHARACTER SET utf8")

    db.close()

##---------------Create Table---------------##
def Create_table():
    db = pymysql.connect(host='localhost', user='root', password='', port=3306, db='Mini_Project3')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS Tweepy_Data (ID VARCHAR(255) NOT NULL, Twitter_ID VARCHAR(255) NOT NULL, Amount INT NOT NULL,' \
          ' Descrition VARCHAR(255) NOT NULL,  PRIMARY KEY (id))'
    cursor.execute(sql)
    db.close()
def Insert_DB(Twitter_ID, url, Img_number, label):
	db = pymysql.connect(host='localhost', user='root', password='', port=3306, db='Mini_Project3')
	cursor = db.cursor()
	# user = input('Enter the username to Insert')
	time = datetime.datetime.now()

	try:

		sql = 'INSERT INTO Tweepy_Data (Twitter_ID,Img_url, Img_number,label,Op_time) VALUES (%s, %s, %s, %s, %s)'
		# Tweepy_Data = {'Twitter_ID': 'Twitter_ID'}

		cursor.execute(sql, (Twitter_ID, url, Img_number, label, time))
		db.commit()
	except:
		db.rollback()
		print("Can't connect to MySQL service")

def query_user(username):
	db = pymysql.connect(host='localhost', user='root', password='', port=3306, db='Mini_Project3')
	cursor = db.cursor()
	sql = "SELECT * FROM Tweepy_Data WHERE Twitter_ID='" + username + "'"
	cursor.execute(sql)
	result = cursor.fetchall()
	if(len(result)==0):
		print("This User Name is Not Found In Table")

	else:
		for user in result:
			print(user)

def show_all():
	db = pymysql.connect(host='localhost', user='root', password='', port=3306, db='Mini_Project3')
	cursor = db.cursor()
	cursor.execute('SELECT * FROM Tweepy_Data')
	results= cursor.fetchall()
	db.commit()
	for user in results:
		print(user)


def searchbykewords(username):
	db = pymysql.connect(host='localhost', user='root', password='', port=3306, db='Mini_Project3')
	cursor = db.cursor()
	# username=input('Enter the username to search')

	sql="SELECT * FROM Tweepy_Data"
	cursor.execute(sql,username)
	result = cursor.fetchall()

	print("Second user already has this word", username, "in description:")
	for user in result:
		desc = user[3]
		desc = desc.split(',')
		if username in desc:
			print(user[1])
	db.close()

def delete_user(username):
	db = pymysql.connect(host='localhost', user='root', password='', port=3306, db='Mini_Project3')
	cursor = db.cursor()
	sql = "DELETE FROM Tweepy_Data WHERE Twitter_ID = %s"
	try:
		cursor.execute(sql,username)
		results = cursor.fetchall()
		db.commit()

	except:
		db.rollback()
		print("This Username is Not Found In Table")
	db.close()

def Clean_table_data():
	db = pymysql.connect(host='localhost', user='root', password='', port=3306, db='Mini_Project3')
	cursor = db.cursor()
	cursor.execute('use Mini_Project3')
	try:
			cursor.execute("DROP TABLE IF EXISTS Tweepy_Data")
			sql = 'CREATE TABLE IF NOT EXISTS Tweepy_Data (ID MEDIUMINT NOT NULL AUTO_INCREMENT, Twitter_ID VARCHAR(255) NOT NULL,Img_url VARCHAR(255) NOT NULL, Img_number INT NOT NULL, label VARCHAR(255) NOT NULL, Op_time CHAR(50) NOT NULL, PRIMARY KEY (ID))'
			cursor.execute(sql)
			db.commit()
	except:
		db.rollback()
	db.close()








