from flask_mysqldb import MySQLdb

db = MySQLdb.connect(host = "localhost", user ="root", passwd = "1616")
cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS db_nursing")
cursor.execute("CREATE DATABASE IF NOT EXISTS db_nursing")
db.close()

db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
cursor = db.cursor()


sql_line =  """CREATE TABLE Nursinghome(
                home_name VARCHAR(40) NOT NULL,
                city VARCHAR(40) NOT NULL ,
                homeid INT AUTO_INCREMENT,
                PRIMARY KEY (homeid)
                )
            """
cursor.execute(sql_line)

sql_line =  """CREATE TABLE Doctor(
                doctor_name VARCHAR(40) NOT NULL,
                email VARCHAR(40) PRIMARY KEY,
                doc_password VARCHAR(64) NOT NULL,
                nursinghomeid INT NOT NULL UNIQUE,
                FOREIGN KEY (nursinghomeid) REFERENCES Nursinghome(homeid)
                    ON DELETE CASCADE 
                    ON UPDATE CASCADE
                )
            """
cursor.execute(sql_line)

sql_line = "INSERT INTO Nursinghome(home_name, city, homeid) VALUES ('Aydın Huzurevi', 'Aydın', 1)"
cursor.execute(sql_line)
sql_line = "INSERT INTO Doctor(doctor_name, email, doc_password,nursinghomeid) VALUES ('Aylin Acar', 'draylinacar@gmail.com','aylin123',1) "
cursor.execute(sql_line)

#sql_line = "SELECT * FROM doctor"
#cursor.execute(sql_line)

