from flask import Flask,render_template,request,redirect,url_for,flash,current_app,session
from datetime import date
from flask_mysqldb import MySQL
from passlib.hash import pbkdf2_sha256 as hasher



def home():
    mysql = current_app.config["mysql"]
    today = date.today()
    date_time = today.strftime("%m/%d/%Y")
    name = None
    residents = None
    nurses = None
    diseases = None
    if "homeid" in session:
        homeid = session["homeid"]
        if homeid != 0:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM Doctor WHERE nursinghomeid=%s",(homeid,))
            data = cursor.fetchone()
            name = data[2]  #doctor name
            cursor.execute("""SELECT Resident.name FROM Resident INNER JOIN Nurse ON Resident.nurseid=Nurse.nurseid 
                        WHERE Nurse.nursinghomeid={0}
                    """.format(homeid) )
            residents = cursor.fetchall()
            cursor.execute("SELECT name FROM Nurse WHERE nursinghomeid={0}".format(homeid))
            nurses = cursor.fetchall()
            cursor.execute("SELECT name FROM Disease WHERE homeid={0}".format(homeid))
            diseases = cursor.fetchall()
            cursor.close()
    return render_template("home.html",date=date_time,name=name, residents=residents,nurses=nurses,diseases=diseases)


def resident_disease_page(residentid):
    mysql = current_app.config["mysql"]
    global LOGGED
    global homeid
    cursor = mysql.connection.cursor()
    if request.method == "GET":
        values = {"startdate": "", "enddate":"","diseaseid":"","note":""}
        cursor.execute("SELECT diseaseid,name FROM Disease WHERE homeid={0}".format(homeid))
        diseases = cursor.fetchall()
        cursor.close()
        default = "0"
        return render_template("resident_disease.html", values = values,islogged=LOGGED,diseases=diseases,default=default)
    else:
        form_disease = request.form["diseaseid"]
        form_startdate = request.form["startdate"]
        form_enddate = request.form["enddate"]
        form_note = request.form["note"]
        note = str(form_note)
        diseaseid = str(form_disease)
        startdate = str(form_startdate)
        enddate = str(form_enddate)
        cursor.execute("SELECT * FROM Diseaseowners WHERE residentid={0} AND diseaseid={1}".format(residentid,diseaseid))
        control = cursor.fetchone()
        if diseaseid == "0":
            flash("You should first add a disease or periodic activity to the system.") 
            return render_template("resident.html",residentid=residentid,islogged=LOGGED)
        else:
            if control is None:
                query = "INSERT INTO Diseaseowners(residentid,diseaseid,startdate,enddate,note) VALUES (%s,%s,%s,%s,%s)"
                data = (residentid,diseaseid,startdate,enddate,note)
                cursor.execute(query, data)
            else:
                cursor.execute("UPDATE Diseaseowners SET startdate='{0}', enddate='{1}',note='{2}' WHERE residentid={3} AND diseaseid={3}".format(startdate,enddate,note,residentid,diseaseid))
        mysql.connection.commit()
        cursor.close()
        return render_template("resident_page", residentid=residentid,islogged=LOGGED)

def disease_add_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            values = {"name": "", "risklevel": "", "period": "", "periodnumber":""}
            cursor.close()
            return render_template(
                "disease_edit.html", values = values
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

            insert_stmt = "INSERT INTO Disease(name,risklevel,period,homeid) VALUES (%s,%s,%s,%s)"
            data = (name,risklevel,period,homeid)
            cursor.execute(insert_stmt, data)
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("diseases_page"))

def diseases_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            query = """SELECT diseaseid,name,period,risklevel FROM Disease 
                        WHERE homeid={0} ORDER BY name
                    """.format(homeid)
            cursor.execute(query)
            values = cursor.fetchall()
            return render_template("diseases.html",values=values)
        else:
            form_disease_ids = request.form.getlist("disease_ids")
            for disease_id in form_disease_ids:
                cursor.execute("SELECT * FROM Disease WHERE diseaseid=%s",(disease_id,) )
                data = cursor.fetchone()
                if data is not None:
                    cursor.execute("SELECT * FROM Diseaseowners WHERE diseaseid=%s",(disease_id,) )
                    data_ = cursor.fetchone()
                    if data_ != None:
                        flash("There is a resident with this disease or activity!")
                    else:
                        cursor.execute("DELETE FROM Disease WHERE diseaseid=%s",(disease_id,) )
                    mysql.connection.commit()
            cursor.close()
            return redirect(url_for("diseases_page"))
   
def disease_page(diseaseid):
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Disease WHERE diseaseid=%s",(diseaseid,) )
        values = cursor.fetchone()
        cursor.execute("SELECT name FROM Disease WHERE diseaseid=%s",(diseaseid,) )
        diseases = cursor.fetchall()
        cursor.close()
        return render_template("disease.html",diseaseid=diseaseid, values=values,diseases=diseases)

def disease_edit_page(diseaseid):
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name,risklevel FROM Disease WHERE diseaseid=%s",(diseaseid,) )
        values_place = cursor.fetchone()
        if request.method == "GET":
            values = {"name": "", "risklevel": "", "period":"", "periodnumber":""}
            return render_template("disease_edit_exist.html", values = values,values_place=values_place)
        else:
        
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
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("disease_page", diseaseid=diseaseid))

def logout_page():
    mysql = current_app.config["mysql"]
    today = date.today()
    date_time = today.strftime("%m/%d/%Y")

    session.pop("homeid",None)
    name = None
    return render_template("home.html",name=name,date=date_time)



def resident_add_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            values = {"name": "", "age": "", "gender": "","tel":"","bedridden":""}
            cursor.execute("SELECT nurseid, name FROM Nurse WHERE capacity >0 AND capacity_exist<capacity AND nursinghomeid=%s",(homeid,))
            nurses = cursor.fetchall()
            default = "0"
            return render_template(
                "resident_edit.html", values = values,nurses=nurses,default=default
                )
        else:
            form_name = request.form["name"]
            form_age = request.form["age"]
            form_gender = request.form["gender"]
            form_tel = request.form["tel"]
            form_bedridden = request.form["bedridden"]
            form_nurseid = request.form["nurseid"] 
            name = str(form_name)
            age = str(form_age)
            gender = str (form_gender)
            tel = str(form_tel)
            bedridden = str(form_bedridden)
            nurseid= str(form_nurseid)
            if nurseid == "0":
                flash("Select a nurse! If there is no nurse in the system yet, please add a nurse first!") 
                return redirect(url_for("resident_add_page"))
            else:
                query = "INSERT INTO Resident(name,age,gender,tel,bedridden,nurseid) VALUES (%s,%s,%s,%s,%s,%s)"
                data = (name,age,gender,tel,bedridden,nurseid)
                cursor.execute(query, data)
                cursor.execute("SELECT capacity_exist FROM Nurse WHERE nurseid=%s",(nurseid,))
                capacity_exist_str = cursor.fetchone()
                capacity_exist = int(capacity_exist_str[0]) + 1
                query = "UPDATE Nurse SET capacity_exist={0} WHERE nurseid={1}".format(capacity_exist,nurseid)
                cursor.execute(query)
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for("residents_page"))

def residents_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            query = """SELECT Resident.residentid, Resident.name,Resident.age,Resident.gender,Resident.bedridden, Resident.tel, Nurse.nursinghomeid 
                        FROM Resident INNER JOIN Nurse ON Resident.nurseid=Nurse.nurseid 
                        WHERE Nurse.nursinghomeid={0} ORDER BY Resident.name
                    """.format(homeid)
            cursor.execute(query)
            values = cursor.fetchall()
            cursor.close()
            return render_template("residents.html",values=values)
        else:
            form_resident_ids = request.form.getlist("resident_ids")
            for resident_id in form_resident_ids:
                cursor.execute("SELECT * FROM Resident WHERE residentid=%s",(resident_id,) )
                data = cursor.fetchone() 
                if data is not None:
                    cursor.execute("DELETE FROM Resident WHERE residentid=%s",(resident_id,) )
                    mysql.connection.commit()
            cursor.close()
            return redirect(url_for("residents_page"))

def resident_page(residentid): 
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            cursor.execute("SELECT * FROM Resident WHERE residentid=%s",(residentid,) )
            values = cursor.fetchone()
            cursor.execute("SELECT name FROM Nurse WHERE nurseid=%s",(values[6],))
            nurse_name = cursor.fetchone()
            query = """SELECT Diseaseowners.diseaseid,Disease.name,Diseaseowners.startdate,Diseaseowners.enddate,Disease.period
                            FROM Disease INNER JOIN Diseaseowners ON Disease.diseaseid=Diseaseowners.diseaseid 
                            WHERE residentid={0}
                        """.format(residentid)
            cursor.execute(query)
            diseases = cursor.fetchall()
            cursor.close()
            return render_template("resident.html",residentid=residentid, values=values,nurse_name=nurse_name,diseases=diseases)
        else:
            form_disease_ids = request.form.getlist("disease_ids")
            for diseaseid in form_disease_ids:
                cursor.execute("SELECT * FROM Diseaseowners WHERE residentid={0} AND diseaseid={1}".format(residentid,diseaseid))
                data = cursor.fetchone() 
                if data is not None:
                    cursor.execute("DELETE FROM Diseaseowners WHERE residentid={0} AND diseaseid={1}".format(residentid,diseaseid))
                    mysql.connection.commit()
            cursor.close()
            return redirect(url_for("resident_page",residentid=residentid))

def resident_edit_page(residentid):
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            values = {"name": "", "age": "", "gender":"","tel":"","bedridden":""}
            cursor.execute("SELECT nurseid, name FROM Nurse WHERE capacity >0 AND capacity_exist<capacity AND nursinghomeid=%s",(homeid,))
            nurses = cursor.fetchall()
            cursor.execute("SELECT nurseid FROM Resident WHERE residentid={0}".format(residentid))
            values = cursor.fetchone()
            default = values[0]
            cursor.execute("SELECT name,age,tel FROM Resident WHERE residentid=%s",(residentid,) )
            values_place = cursor.fetchone()
            return render_template("resident_edit_exist.html", values = values,values_place=values_place,nurses=nurses,default=default)
        else:
            form_name = request.form["name"]
            form_age = request.form["age"]
            form_gender = request.form["gender"]
            form_tel = request.form["tel"]
            form_bedridden = request.form["bedridden"]
            form_nurseid = request.form["nurseid"] 
            name = str(form_name)
            gender = str(form_gender)
            tel = str(form_tel)
            age = str (form_age)
            bedridden = str(form_bedridden)
            nurseid = str(form_nurseid)

            cursor.execute("SELECT nurseid FROM Resident WHERE residentid= %s",(residentid,) )
            values = cursor.fetchone()
            old_nurseid = str(values[0])
            if old_nurseid != nurseid:
                cursor.execute("SELECT capacity_exist FROM Nurse WHERE nurseid=%s",(old_nurseid,)) 
                capacity_exist_str = cursor.fetchone()
                capacity_exist = int(capacity_exist_str[0]) -1 
                cursor.execute("UPDATE Nurse SET capacity_exist={0} WHERE nurseid={1}".format(capacity_exist,old_nurseid))

                cursor.execute("SELECT capacity_exist FROM Nurse WHERE nurseid=%s",(nurseid,)) 
                capacity_exist_str = cursor.fetchone()
                capacity_exist = int(capacity_exist_str[0]) +1 
                cursor.execute("UPDATE Nurse SET capacity_exist={0} WHERE nurseid={1}".format(capacity_exist,nurseid))
            
            query = "UPDATE Resident SET name='{0}', age={1}, gender='{2}', tel='{3}', bedridden='{4}', nurseid={5} WHERE residentid={6}".format(name, age, gender ,tel, bedridden,nurseid ,residentid)
            cursor.execute(query)
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("resident_page", residentid=residentid))

def nurses_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            cursor.execute("SELECT nurseid, name,capacity,type,address,tel FROM Nurse WHERE nursinghomeid=%s ORDER BY name",(homeid,))
            values = cursor.fetchall()
            cursor.close()
            return render_template("nurses.html",values=values)
        else:
            form_nurse_ids = request.form.getlist("nurse_ids")
            for nurse_id in form_nurse_ids:
                cursor.execute("SELECT * FROM Nurse WHERE nurseid=%s",(nurse_id,) )
                data = cursor.fetchone()
                if data is not None:
                    cursor.execute("SELECT * FROM Resident WHERE nurseid=%s",(nurse_id,) )
                    data_ = cursor.fetchone()
                    if data_ != None:
                        flash("There are resident(s) assigned to this nurse. Please delete the resident(s) first!")
                    else:
                        cursor.execute("DELETE FROM Nurse WHERE nurseid=%s",(nurse_id,) )
                    mysql.connection.commit()
            cursor.close()
            return redirect(url_for("nurses_page"))

def nurse_add_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        if request.method == "GET":
            values = {"name": "", "capacity": "", "type":"","tel":"","address":""}
            return render_template("nurse_edit.html", values = values)
        else:
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
            exist = 0
            capacity_exist = str(exist)
            cursor = mysql.connection.cursor()
            insert_stmt = "INSERT INTO Nurse(name,capacity,capacity_exist,type,address,tel,nursinghomeid) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            data = (name,capacity,capacity_exist,type_,address,tel,homeid)
            cursor.execute(insert_stmt, data)
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("nurses_page"))
        
def nurse_page(nurseid): 
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Nurse WHERE nurseid=%s",(nurseid,) )
        values = cursor.fetchone()
        cursor.execute("SELECT name FROM Resident WHERE nurseid=%s",(nurseid,) )
        residents = cursor.fetchall()
        cursor.close()
        return render_template("nurse.html",nurseid=nurseid, values=values,residents=residents)

def nurse_edit_page(nurseid):
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            cursor.execute("SELECT capacity_exist FROM Nurse WHERE nurseid=%s",(nurseid,) )
            capacity_exist = cursor.fetchone()
            values = {"name": "", "capacity": "", "type":"","tel":"","address":""}
            return render_template("nurse_edit_exist.html", values = values,islogged=LOGGED,capacity=capacity_exist)
        else:
        
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
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("nurse_page", nurseid=nurseid))
    


def signup_page():
    mysql = current_app.config["mysql"]
    if request.method == "GET":
        values = {"name": "", "homename": "","city":"", "email":"","password":"", "password2":"",
        "type":"", "address":"", "tel":""
        }
        return render_template("signup.html", values = values,)
    else:
        cursor = mysql.connection.cursor()
        #cursor.execute("DROP TABLE IF EXISTS Diseaseowners")
        #cursor.execute("DROP TABLE IF EXISTS Resident")
        #cursor.execute("DROP TABLE IF EXISTS Nurse")
        #cursor.execute("DROP TABLE IF EXISTS Disease")
        #cursor.execute("DROP TABLE IF EXISTS Doctor")
        #cursor.execute("DROP TABLE IF EXISTS Nursinghome")
        
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
                        capacity_exist INT,
                        type VARCHAR(40) NOT NULL,
                        address VARCHAR(90) NOT NULL,
                        tel VARCHAR(40) NOT NULL,
                        nursinghomeid  INT NOT NULL,
                        FOREIGN KEY (nursinghomeid) 
                        REFERENCES Nursinghome(homeid)
                        ON DELETE CASCADE 
                        ON UPDATE CASCADE,
                        PRIMARY KEY (nurseid))""")
        
      
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


        cursor.execute("""CREATE TABLE IF NOT EXISTS Resident(residentid INT AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        age INT NOT NULL,
                        bedridden VARCHAR(40) NOT NULL,
                        gender VARCHAR(20) NOT NULL,
                        tel VARCHAR(40) NOT NULL,
                        nurseid  INT NOT NULL,
                        FOREIGN KEY (nurseid) 
                        REFERENCES Nurse(nurseid)
                        ON DELETE RESTRICT 
                        ON UPDATE CASCADE,
                        PRIMARY KEY (residentid))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Diseaseowners(residentid INT NOT NULL,
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
                                note VARCHAR(100) NOT NULL,
                                PRIMARY KEY(residentid , diseaseid))""")
     
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
        
        line1 = "INSERT INTO Nursinghome(name,city,type,address,tel) VALUES (%s,%s,%s,%s,%s)"
        data1 = (homename,city,type_,address,tel)
        cursor.execute(line1, data1)

        query = "SELECT LAST_INSERT_ID()" 
        cursor.execute(query)
        homeid = cursor.fetchall()

        line2 = "INSERT INTO Doctor(name,email,password,nursinghomeid) VALUES (%s,%s,%s,%s)"
        data2 = (name,email,hashed_password,homeid)
        cursor.execute(line2, data2)
        mysql.connection.commit()
        cursor.close()
    flash("Account created!")
    return render_template("login_html",islogged=islogged)

def login_page():
    mysql = current_app.config["mysql"]
    if request.method == "GET":
        values = {"email":"","password":""}
        return render_template("login.html", values = values)
    else:
        form_email = request.form["email"]
        form_password = request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Doctor WHERE email=%s",(form_email,) )
        data = cursor.fetchone()
        cursor.close()
        if data is not None:
            if hasher.verify(form_password,data[3]):
                homeid_db = data[4] #nursinghome id
                doctorid_db = data[0]  #doctor id
                name = data[2]
                homeid = homeid_db
                doctorid = doctorid_db
                today = date.today()
                date_time = today.strftime("%m/%d/%Y")
                
                flash("You have logged in.")

                session["homeid"] = homeid_db
                mysql.connection.commit()
                cursor.close()
                return render_template("home.html",name=name,date=date_time)
            else:
                flash("Wrong Password!")
                return redirect(url_for("login_page"))
        else:
            flash("Wrong Email!")
            return redirect(url_for("login_page"))

def filter_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT  Disease.name ,COUNT(residentid)
                    FROM Diseaseowners INNER JOIN Disease ON Disease.diseaseid=Diseaseowners.diseaseid
                    WHERE Disease.homeid={0}
                    GROUP BY Diseaseowners.diseaseid """.format(homeid))
        result = dict(cursor.fetchall())
        cursor.execute("SELECT diseaseid,name FROM Disease WHERE homeid={0}".format(homeid))
        diseases = cursor.fetchall()
        residents = None
        residents2 = None
        if request.method == "GET":
            default = "0"
            return render_template("filter.html", diseases=diseases,residents=residents,residents2=residents2, default=default,result=result)
        else:
            if 'filter_disease' in request.form:
                form_diseaseid = request.form["diseaseid"] 
                diseaseid = str(form_diseaseid)
                if diseaseid == "0":
                    flash("Select a disease! If there is no disease in the system yet, please add a disease first!") 
                    return redirect(url_for("filter_page"))
                else:
                    query = """SELECT Resident.residentid, Resident.name
                                    FROM Resident INNER JOIN Diseaseowners ON Resident.residentid=Diseaseowners.residentid 
                                    WHERE diseaseid={0}
                                """.format(form_diseaseid)
                    cursor.execute(query) 
                    residents = cursor.fetchall()
                    cursor.execute("SELECT diseaseid,name FROM Disease WHERE homeid={0}".format(homeid))
                    diseases = cursor.fetchall()
                    cursor.execute("SELECT name FROM Disease WHERE diseaseid={0}".format(form_diseaseid))
                    diseasename = cursor.fetchone()

                    cursor.close()
                    return render_template("filter.html",result=result,residents=residents,residents2=residents2,diseases=diseases,diseasename =diseasename)
            else:
                risklevel = 5
                query = """SELECT DISTINCT Resident.name
                                    FROM Resident INNER JOIN Diseaseowners ON Resident.residentid=Diseaseowners.residentid 
                                    INNER JOIN Disease ON Disease.diseaseid=Diseaseowners.diseaseid
                                    WHERE Disease.risklevel={0}
                                """.format(risklevel)
                cursor.execute(query) 
                residents2 = cursor.fetchall()
                return render_template("filter.html",result=result,residents=residents,residents2=residents2,diseases=diseases)
    else:
        return redirect(url_for("login_page"))

def review_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT period FROM Disease WHERE homeid={0}".format(homeid))
        periods = cursor.fetchall()
        default = "0"
        if request.method == "GET":
            cursor.close()
            return render_template("review.html", periods=periods,default=default)
        else:
            form_period = request.form["period"] 
            period = str (form_period)
            if period == "0":
                flash("Select a period! If there is no periodic activity in the system yet, please add a periodic activity first!") 
                return redirect(url_for("review_page"))
            else:
                query = "SELECT name FROM Disease WHERE period='{0}' and homeid={1}".format(form_period,homeid)
                cursor.execute(query)
                diseasenames = cursor.fetchall()
                cursor.close()
                return render_template("review.html", periods=periods,diseasenames =diseasenames,period=form_period)
    else:
        return redirect(url_for("login_page"))

def profile_page():
    mysql = current_app.config["mysql"]   
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            cursor.execute("""SELECT Doctor.name,Doctor.email,Nursinghome.name,Nursinghome.city,Nursinghome.address,
                                Nursinghome.type, Nursinghome.tel
                            FROM Doctor INNER JOIN Nursinghome ON Doctor.nursinghomeid=Nursinghome.homeid 
                            WHERE Doctor.nursinghomeid={0}
                    """.format(homeid) )
            values= cursor.fetchone()
            return render_template("profile.html", islogged=LOGGED,values=values)
        else:
            session.pop("homeid",None)
            name = None
            today = date.today()
            date_time = today.strftime("%m/%d/%Y")
            cursor.execute("DELETE FROM Doctor WHERE nursinghomeid=%s",(homeid,) )
            cursor.execute("DELETE FROM Nursinghome WHERE homeid=%s",(homeid,) )
        
            mysql.connection.commit()
            cursor.close()
            return render_template("home.html",name=name,date=date_time)

def profile_edit_page():
    mysql = current_app.config["mysql"]
    if "homeid" in session:
        homeid = session["homeid"]
        cursor = mysql.connection.cursor()
        if request.method == "GET":
            values = {"dr_name": "", "h_name": "", "email":"","tel":"","address":"","city":"","type":""}
            return render_template("profile_edit.html", values = values)
        else:
            form_dr_name = request.form["dr_name"]
            form_h_name = request.form["h_name"]
            form_email = request.form["email"]
            form_type = request.form["type"]
            form_tel = request.form["tel"]
            form_address = request.form["address"]
            form_city = request.form["city"]
     
            dr_name = str(form_dr_name)
            h_name = str(form_h_name)
            email = str(form_email)
            type_ = str (form_type)
            tel = str(form_tel)
            address = str(form_address)
            city = str(form_city)

            query = "UPDATE Doctor SET name='{0}', email='{1}' WHERE nursinghomeid={2}".format(dr_name, email,homeid)
            cursor.execute(query)
            query = "UPDATE Nursinghome SET name='{0}', city='{1}', type='{2}', tel='{3}', address='{4}' WHERE homeid={5}".format(h_name, city, type_ ,tel, address, homeid)
            cursor.execute(query)

            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("profile_page"))