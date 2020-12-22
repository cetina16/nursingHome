from flask_mysqldb import MySQLdb

db = MySQLdb.connect(host = "localhost", user ="root", passwd = "1616")
cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS db_nursing")
cursor.execute("CREATE DATABASE IF NOT EXISTS db_nursing")
db.close()

db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
cursor = db.cursor()

sql_line =  """CREATE TABLE DOCTOR(
                nh_id INT PRIMARY KEY AUTO_INCREMENT,
                doctor_name VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL UNIQUE,
                doc_password VARCHAR(64) NOT NULL
                )
            """
cursor.execute(sql_line)


sql_line = "INSERT INTO DOCTOR(nh_id,doctor_name, email, doc_password) VALUES (1,'Aylin Acar', 'draylinacar@gmail.com','aylin123') "
cursor.execute(sql_line)

