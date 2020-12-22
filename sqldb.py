from flask_mysqldb import MySQLdb

db = MySQLdb.connect(host = "localhost", user ="root", passwd = "1616")
cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS db_nursing")
cursor.execute("CREATE DATABASE IF NOT EXISTS db_nursing")
db.close()

db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
cursor = db.cursor()

sql_line =  """CREATE TABLE DOCTOR(
                doctor_name VARCHAR(40) NOT NULL,
                email VARCHAR(40) PRIMARY KEY,
                doc_password VARCHAR(64) NOT NULL,
                nh_id INT NOT NULL UNIQUE
                )
            """
cursor.execute(sql_line)


sql_line = "INSERT INTO DOCTOR(nh_id,doctor_name, email, doc_password) VALUES (1,'Aylin Acar', 'draylinacar@gmail.com','aylin123') "
cursor.execute(sql_line)

