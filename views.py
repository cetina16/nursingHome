from flask import render_template,request,redirect,url_for,flash
from datetime import date
from flask import current_app
from passlib.hash import pbkdf2_sha256 as hasher
from flask_mysqldb import MySQLdb

homeid = 0
doctorid = 0
LOGGED = False

def home():
    today = date.today()
    date_time = today.strftime("%m/%d/%Y")
    name = None
    global homeid
    if homeid != 0:
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Doctor WHERE nursinghomeid=%s",(homeid,))
        data = cursor.fetchone()
        cursor.close()
        name = data[2]  #doctor name
    return render_template("home.html",islogged=LOGGED ,date=date_time,name=name)

def resident_disease_page(residentid):
    global LOGGED
    global homeid
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    if request.method == "GET":
        values = {"startdate": "", "enddate":"","diseaseid":""}
        cursor.execute("SELECT diseaseid,name FROM Disease WHERE homeid=%s",(homeid,))
        diseases = cursor.fetchall()
        cursor.close()
        return render_template("resident_disease.html", values = values,islogged=LOGGED,diseases=diseases)
    else:
        form_disease = request.form["diseaseid"]
        form_startdate = request.form["startdate"]
        form_enddate = request.form["enddate"]
        diseaseid = str(form_disease)
        startdate = str(form_startdate)
        enddate = str(form_enddate)
   
        query = "INSERT INTO Diseaseowners(residentid,diseaseid,startdate,enddate) VALUES (%s,%s,%s,%s)"
        data = (residentid,diseaseid,startdate,enddate)
        cursor.execute(query, data)
  

       
        db.commit()
        cursor.close()
        return redirect(url_for("resident_page", residentid=residentid,islogged=LOGGED))

def disease_add_page():
    global LOGGED
    global homeid
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    if request.method == "GET":
        values = {"name": "", "risklevel": "", "period": "", "periodnumber":""}
        return render_template(
            "disease_edit.html", values = values,islogged=LOGGED
        )
    else:
        form_name = request.form["name"]
        form_risklevel = request.form["risklevel"]
        form_period = request.form["period"]
        form_period_number = request.form["periodnumber"]

        name = str(form_name)
        risklevel = str(form_risklevel)
        period_type = str (form_period)
        period_number= str(form_period_number)
        period = period_number +" "+ period_type

        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()

        insert_stmt = "INSERT INTO Disease(name,risklevel,period,homeid) VALUES (%s,%s,%s,%s)"
        data = (name,risklevel,period,homeid)
        cursor.execute(insert_stmt, data)
        db.commit()
        cursor.close()
        return redirect(url_for("diseases_page"))

def diseases_page():
    global LOGGED
    global homeid
    if request.method == "GET":
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        query = """SELECT diseaseid,name,period,risklevel FROM Disease 
                    WHERE homeid={0}
                """.format(homeid)
        cursor.execute(query)
        values = cursor.fetchall()
        return render_template("diseases.html",values=values,islogged=LOGGED)
    else:
        form_disease_ids = request.form.getlist("disease_ids")
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        for disease_id in form_disease_ids:
            cursor.execute("SELECT * FROM Disease WHERE diseaseid=%s",(disease_id,) )
            data = cursor.fetchone()
            if data is not None:
                cursor.execute("DELETE FROM Disease WHERE diseaseid=%s",(disease_id,) )
                db.commit()
        cursor.close()
        return redirect(url_for("diseases_page"))
   

def disease_page(diseaseid):
    global LOGGED
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Disease WHERE diseaseid=%s",(diseaseid,) )
    values = cursor.fetchone()
    cursor.execute("SELECT name FROM Disease WHERE diseaseid=%s",(diseaseid,) )
    diseases = cursor.fetchall()
    cursor.close()
    return render_template("disease.html",diseaseid=diseaseid, values=values,islogged=LOGGED,diseases=diseases)

def disease_edit_page(diseaseid):
    global LOGGED
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    cursor.execute("SELECT name,risklevel FROM Disease WHERE diseaseid=%s",(diseaseid,) )
    values_place = cursor.fetchone()
    if request.method == "GET":
        values = {"name": "", "risklevel": "", "period":"", "periodnumber":""}
        return render_template("disease_edit_exist.html", values = values,islogged=LOGGED,values_place=values_place)
    else:
        global homeid
        form_name = request.form["name"]
        form_risklevel = request.form["risklevel"]
        form_period = request.form["period"]
        form_period_number = request.form["periodnumber"]

        name = str(form_name)
        risklevel = str(form_risklevel)
        period_type = str (form_period)
        period_number= str(form_period_number)
        period = period_number + period_type

    
        query = "UPDATE Disease SET name='{0}', risklevel={1}, period='{2}' WHERE diseaseid={3}".format(name, risklevel, period,diseaseid)
        cursor.execute(query)
        db.commit()
        cursor.close()
        return redirect(url_for("disease_page", diseaseid=diseaseid,islogged=LOGGED))


def logout_page():
    today = date.today()
    date_time = today.strftime("%m/%d/%Y")
    global homeid
    global doctorid
    global LOGGED
    LOGGED = False
    doctorid = 0
    homeid = 0
    name = None
    return render_template("home.html",islogged=LOGGED,name=name,date=date_time)

def resident_add_page():
    global LOGGED
    global homeid
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    if request.method == "GET":
        values = {"name": "", "age": "", "gender": "","tel":"","bedridden":""}
        cursor.execute("SELECT nurseid, name FROM Nurse WHERE capacity >0 AND nursinghomeid=%s",(homeid,))
        nurses = cursor.fetchall()
        return render_template(
            "resident_edit.html", values = values,islogged=LOGGED,nurses=nurses
        )
    else:
        form_name = request.form["name"]
        form_age = request.form["age"]
        form_gender = request.form["gender"]
        form_tel = request.form["tel"]
        form_bedridden = request.form["bedridden"]
        form_nurseid = request.form["nurseid"]    # FIX!!!!!!!!!!!!!
        name = str(form_name)
        age = str(form_age)
        gender = str (form_gender)
        tel = str(form_tel)
        bedridden = str(form_bedridden)
        nurseid= str(form_nurseid)

        insert_stmt = "INSERT INTO Resident(name,age,gender,tel,bedridden,nurseid) VALUES (%s,%s,%s,%s,%s,%s)"
        data = (name,age,gender,tel,bedridden,nurseid)
        cursor.execute(insert_stmt, data)
        db.commit()
        cursor.close()
        return redirect(url_for("residents_page"))

def residents_page():
    global LOGGED
    global homeid
    if request.method == "GET":
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        #JOIN 
        query = """SELECT Resident.residentid, Resident.name,Resident.age,Resident.gender,Resident.bedridden, Resident.tel, Nurse.nursinghomeid 
                    FROM Resident INNER JOIN Nurse ON Resident.nurseid=Nurse.nurseid 
                    WHERE Nurse.nursinghomeid={0}
                """.format(homeid)
        cursor.execute(query)
        values = cursor.fetchall()
        return render_template("residents.html",values=values,islogged=LOGGED)
    else:
        form_resident_ids = request.form.getlist("resident_ids")
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        for resident_id in form_resident_ids:
            cursor.execute("SELECT * FROM Resident WHERE residentid=%s",(resident_id,) )
            data = cursor.fetchone() 
            if data is not None:
                cursor.execute("DELETE FROM Resident WHERE residentid=%s",(resident_id,) )
                db.commit()
        cursor.close()
        return redirect(url_for("residents_page"))

def resident_page(residentid): 
    global LOGGED
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Resident WHERE residentid=%s",(residentid,) )
    values = cursor.fetchone()
    cursor.execute("SELECT name FROM Nurse WHERE nurseid=%s",(values[6],))
    nurse_name = cursor.fetchone()
    query = """SELECT Diseaseowners.diseaseid,Disease.name,Diseaseowners.startdate,Diseaseowners.enddate
                    FROM Disease INNER JOIN Diseaseowners ON Disease.diseaseid=Diseaseowners.diseaseid 
                    WHERE residentid={0}
                """.format(residentid)
    cursor.execute(query)
    diseases = cursor.fetchall()

    cursor.close()
    return render_template("resident.html",residentid=residentid, values=values,nurse_name=nurse_name,islogged=LOGGED,diseases=diseases)

def resident_edit_page(residentid):
    global LOGGED
    global homeid
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    if request.method == "GET":
        values = {"name": "", "age": "", "gender":"","tel":"","bedridden":""}
        cursor.execute("SELECT nurseid, name FROM Nurse WHERE capacity >0 AND nursinghomeid=%s",(homeid,))
        nurses = cursor.fetchall()
        return render_template("resident_edit_exist.html", values = values,islogged=LOGGED,nurses=nurses)
    else:
        form_name = request.form["name"]
        form_age = request.form["age"]
        form_gender = request.form["gender"]
        form_tel = request.form["tel"]
        form_bedridden = request.form["bedridden"]
        name = str(form_name)
        gender = int(form_gender)
        tel = str(form_tel)
        age = str (form_age)
        bedridden = str(form_bedridden)

        query = "UPDATE Resident SET name='{0}', age={1}, gender='{2}', tel='{3}', bedridden='{4}' WHERE residentid={5}".format(name, age, gender ,tel, bedridden, residentid)
        cursor.execute(query)
        db.commit()
        cursor.close()
        return redirect(url_for("resident_page", residentid=residentid,islogged=LOGGED))
def nurses_page():
    if request.method == "GET":
        global homeid
        global LOGGED
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        cursor.execute("SELECT nurseid, name,capacity,type,address,tel FROM Nurse WHERE nursinghomeid=%s",(homeid,))
        values = cursor.fetchall()
        return render_template("nurses.html",values=values,islogged=LOGGED)
    else:
        form_nurse_ids = request.form.getlist("nurse_ids")
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
       
        for nurse_id in form_nurse_ids:
            cursor.execute("SELECT * FROM Nurse WHERE nurseid=%s",(nurse_id,) )
            data = cursor.fetchone()
            if data is not None:
                cursor.execute("DELETE FROM Nurse WHERE nurseid=%s",(nurse_id,) )
                db.commit()
        cursor.close()
        return redirect(url_for("nurses_page"))

def nurse_add_page():
    global LOGGED
    if request.method == "GET":
        values = {"name": "", "capacity": "", "type":"","tel":"","address":""}
        return render_template("nurse_edit.html", values = values,islogged=LOGGED)
    else:
        global homeid
        form_name = request.form["name"]
        form_capacity = request.form["capacity"]
        form_type = request.form["type"]
        form_tel = request.form["tel"]
        form_address = request.form["address"]
        name = str(form_name)
        capacity = str(form_capacity)
        type_ = str (form_type)
        tel = str(form_tel)
        address = str(form_address)

        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()

        insert_stmt = "INSERT INTO Nurse(name,capacity,type,address,tel,nursinghomeid) VALUES (%s,%s,%s,%s,%s,%s)"
        data = (name,capacity,type_,address,tel,homeid)
        cursor.execute(insert_stmt, data)
        db.commit()
        cursor.close()
        return redirect(url_for("nurses_page"))
        
def nurse_page(nurseid): 
    global LOGGED
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Nurse WHERE nurseid=%s",(nurseid,) )
    values = cursor.fetchone()
    cursor.execute("SELECT name FROM Resident WHERE nurseid=%s",(nurseid,) )
    residents = cursor.fetchall()
    cursor.close()
    return render_template("nurse.html",nurseid=nurseid, values=values,islogged=LOGGED,residents=residents)

def nurse_edit_page(nurseid):
    global LOGGED
    if request.method == "GET":
        values = {"name": "", "capacity": "", "type":"","tel":"","address":""}
        return render_template("nurse_edit_exist.html", values = values,islogged=LOGGED)
    else:
        global homeid
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        form_name = request.form["name"]
        form_capacity = request.form["capacity"]
        form_type = request.form["type"]
        form_tel = request.form["tel"]
        form_address = request.form["address"]
        name = str(form_name)
        capacity = int(form_capacity)
        type_ = str (form_type)
        tel = str(form_tel)
        address = str(form_address)

        query = "UPDATE Nurse SET name='{0}', capacity={1}, type='{2}', tel='{3}', address='{4}' WHERE nurseid={5}".format(name, capacity, type_ ,tel, address, nurseid)
        cursor.execute(query)
        db.commit()
        cursor.close()
        return redirect(url_for("nurse_page", nurseid=nurseid,islogged=LOGGED))
 

def filter_page():
    return render_template("filter.html",islogged=LOGGED)
def review_page():
    return render_template("review.html",islogged=LOGGED)
    
def signup_page():
    if request.method == "GET":
        values = {"name": "", "homename": "","city":"", "email":"","password":"", "password2":"",
        "type":"", "address":"", "tel":""
        }
        return render_template("signup.html", values = values,)
    else:
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        #cursor.execute("DROP TABLE IF EXISTS Doctor")
       # cursor.execute("DROP TABLE IF EXISTS Resident")
       # cursor.execute ("DROP TABLE IF EXISTS Nurse")
       # cursor.execute("DROP TABLE IF EXISTS Disease")
       # cursor.execute("DROP TABLE IF EXISTS Nursinghome")
       
        form_name = request.form["name"] 
        form_homename = request.form["homename"]
        form_city = request.form["city"]
        form_email = request.form["email"]
        form_password = request.form["password"]
        form_password2 = request.form["password2"]
        form_address = request.form["address"]
        form_tel = request.form["tel"]
        form_type = request.form["type"]

        cursor.execute("SELECT * FROM Doctor WHERE email=%s",(form_email,) )
        data = cursor.fetchone()
        if data is not None:
            flash("This email is registered in the system!")
            return redirect(request.url)
        if not len(form_password) >= 4:
            flash("Password must be at least 4 characters!")
            return redirect(request.url)
        if form_password != form_password2:
            flash("Please verify password!")
            return redirect(request.url)

        name = str(form_name)
        homename = str(form_homename)
        city = str(form_city)
        email = str(form_email)
        password = str (form_password)
        address = str(form_address)
        type_ = str (form_type)
        tel = str(form_tel)

        hashed_password = hasher.hash(password)
    
    
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS Nursinghome(homeid INT AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        city VARCHAR(40) NOT NULL,
                        type VARCHAR(40) NOT NULL,
                        address VARCHAR(40) NOT NULL,
                        tel VARCHAR(40) NOT NULL,
                        PRIMARY KEY (homeid))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Doctor(doctorid INT AUTO_INCREMENT,
                            email VARCHAR(40) UNIQUE,
                            name VARCHAR (40) NOT NULL ,
                            password VARCHAR (100)  NOT NULL ,
                            nursinghomeid INT,
                            FOREIGN KEY (nursinghomeid)  
                            REFERENCES Nursinghome(homeid) 
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                            PRIMARY KEY (doctorid))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Nurse(nurseid INT AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        capacity INT NOT NULL,
                        type VARCHAR(40) NOT NULL,
                        address VARCHAR(90) NOT NULL,
                        tel VARCHAR(40) NOT NULL,
                        nursinghomeid  INT NOT NULL,
                        FOREIGN KEY (nursinghomeid) 
                        REFERENCES Nursinghome(homeid)
                        ON DELETE CASCADE 
                        ON UPDATE CASCADE,
                        PRIMARY KEY (nurseid))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Resident(residentid INT AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        age INT NOT NULL,
                        bedridden VARCHAR(40) NOT NULL,
                        gender VARCHAR(20) NOT NULL,
                        tel VARCHAR(40) NOT NULL,
                        nurseid  INT NOT NULL,
                        FOREIGN KEY (nurseid) 
                        REFERENCES Nurse(nurseid)
                        ON DELETE CASCADE 
                        ON UPDATE CASCADE,
                        PRIMARY KEY (residentid))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Disease(diseaseid INT AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        risklevel INT NOT NULL,
                        period VARCHAR(40) NOT NULL,
                        homeid INT NOT NULL,
                        FOREIGN KEY (homeid) 
                        REFERENCES Nursinghome(homeid)
                        ON DELETE CASCADE 
                        ON UPDATE CASCADE,
                        PRIMARY KEY (diseaseid))""")
        
        line1 = "INSERT INTO Nursinghome(name,city,type,address,tel) VALUES (%s,%s,%s,%s,%s)"
        data1 = (homename,city,type_,address,tel)
        cursor.execute(line1, data1)

        query = "SELECT LAST_INSERT_ID()" 
        cursor.execute(query)
        homeid = cursor.fetchall()

        line2 = "INSERT INTO Doctor(name,email,password,nursinghomeid) VALUES (%s,%s,%s,%s)"
        data2 = (name,email,hashed_password,homeid)
        cursor.execute(line2, data2)
        db.commit()
        cursor.close()
    flash("Account created!")
    return redirect(url_for("login_page"))

def login_page():
    global LOGGED
    if request.method == "GET":
        values = {"email":"","password":""}
        return render_template("login.html", values = values,islogged=LOGGED)
    else:
        form_email = request.form["email"]
        form_password = request.form["password"]

        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Doctor WHERE email=%s",(form_email,) )

        data = cursor.fetchone()
        cursor.close()
        global homeid 
        global doctorid
        if data is not None:
            if hasher.verify(form_password,data[3]):
                homeid_db = data[4] #nursinghome id
                doctorid_db = data[0]  #doctor id
                name = data[2]
                homeid = homeid_db
                doctorid = doctorid_db
                today = date.today()
                date_time = today.strftime("%m/%d/%Y")
                LOGGED = True
                islogged = LOGGED
                flash("You have logged in.")
                db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
                cursor = db.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS DiseaseOwners(residentid INT NOT NULL,
                                diseaseid INT NOT NULL,
                                FOREIGN KEY (residentid)	
                                REFERENCES Resident(residentid)
                                ON DELETE CASCADE 
                                ON UPDATE CASCADE,
                                FOREIGN KEY (diseaseid)	
                                REFERENCES Disease (diseaseid)
                                ON DELETE RESTRICT
                                ON UPDATE CASCADE,
                                startdate DATE NOT NULL,
                                enddate DATE,
                                PRIMARY KEY(residentid , diseaseid))""")
                db.commit()
                cursor.close()
                return render_template("home.html",islogged=islogged,name=name,date=date_time)
            else:
                islogged = LOGGED
                flash("Wrong Password!")
                return redirect(url_for("login_page",islogged=islogged))
        else:
            islogged = LOGGED
            flash("Wrong Email!")
            return redirect(url_for("login_page",islogged=islogged))




     
