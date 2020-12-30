from flask import render_template,request,redirect,url_for
from datetime import date
from flask import current_app
from disease import Disease
from resident import Resident
from forms import LoginForm
from user import get_user
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import login_user,logout_user
from flask_mysqldb import MySQLdb

def home():
    today = date.today()
    date_time = today.strftime("%m/%d/%Y")
    return render_template("home.html", date=date_time)

def disease_add_page():
    if request.method == "GET":
        values = {"name": "", "risklevel": "", "period": ""}
        return render_template(
            "disease_edit.html", values = values,
        )
    else:
        form_name = request.form["name"]
        form_risk = request.form["risklevel"]
        form_period = request.form["period"]
        disease = Disease(form_name, risklevel = int(form_risk),period=int(form_period) if form_period else None)

        db = current_app.config["db"]
        disease_key = db.add_disease(disease)
        #return render_template("disease_edit.html")
        return redirect(url_for("diseases_page"))

def diseases_page():
    db = current_app.config["db"]
    if request.method == "GET":
        diseases = db.get_diseases()
        return render_template("diseases.html", diseases=sorted(diseases)) 
    else:
        form_disease_keys = request.form.getlist("disease_keys")
        for form_disease_key in form_disease_keys:
            db.delete_disease(int(form_disease_key))
        #return render_template("home.html")
        return redirect(url_for("diseases_page"))

def disease_page(disease_key):
    db = current_app.config["db"]
    disease = db.get_disease(disease_key)
    return render_template("disease.html", disease=disease)

def disease_edit_page(disease_key):
    if request.method == "GET":
        db = current_app.config["db"]
        disease = db.get_disease(disease_key)
        if disease is None:
            abort(404)
        values = {"name": disease.name, "risklevel": disease.risklevel, "period":disease.period}
        return render_template(
            "disease_edit.html",
            values=values,
        )
    else:
        form_name = request.form["name"]
        form_risklevel = request.form["risklevel"]
        form_period = request.form["period"]
        disease = Disease(form_name,risklevel=int(form_risklevel), period=int(form_period) if form_period else None)
        db = current_app.config["db"]
        db.update_disease(disease_key, disease)
        return redirect(url_for("disease_page", disease_key=disease_key))

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data["email"]
        user = get_user(email)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                #flash("You have logged in.")
                next_page = request.args.get("next", url_for("home"))
                return redirect(next_page)
        #flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    #flash("You have logged out.")
    return redirect(url_for("home"))

def resident_add_page():
    if request.method == "GET":
        values = {"name": "", "age": "", "gender": ""}
        return render_template(
            "resident_edit.html", values = values,
        )
    else:
        form_name = request.form["name"]
        form_age = request.form["age"]
        form_gender = request.form["gender"]
        name = str(form_name)
        age = int (form_age)
        gender = str(form_gender)

        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        #insert_stmt = ("INSERT INTO Resident(name, age, gender)" "VALUES (name,age,gender)")
        
        #data = (name,age,gender)
        #cursor.execute(insert_stmt, data)
        # cursor.execute("INSERT INTO Resident(name, age, gender) VALUES (%s,%s,%s))
        cursor.execute("INSERT INTO Resident(name, age, gender,) VALUES(%s,%d,%s)", (form_name,form_age,form_gender))
        # line = "INSERT INTO Resident(name, age, gender) VALUES (%s,%s,%s)"
        #cursor.execute(line,(form_name,form_age,form_gender))
        db.commit()
        cursor.close()
       # return redirect(url_for("resident_add_page"))
        return "success"

def residents_page():
    if request.method == "GET":
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        query = "SELECT name,age,gender FROM resident"
        cursor.execute(query)
        values = cursor.fetchall()
        return render_template("residents.html",values=values)
    else:
        return redirect(url_for("residents_page"))

def nurses_page():
    if request.method == "GET":
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        query = "SELECT name,capacity FROM nurse"
        cursor.execute(query)
        values = cursor.fetchall()
        return render_template("nurses.html",values=values)
    else:
        return redirect(url_for("nurses_page"))

def nurse_add_page():
    if request.method == "GET":
        values = {"name": "", "capacity": ""}
        return render_template(
            "nurse_edit.html", values = values,
        )
    else:
        form_name = request.form["name"]
        form_capacity = request.form["capacity"]
        name = str(form_name)
        capacity = str(form_capacity)
        homeid = "1"
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()

        insert_stmt = "INSERT INTO Nurse(name,capacity) VALUES (%s,%s)"
        data = (name,capacity)
        cursor.execute(insert_stmt, data)

        db.commit()
        cursor.close()
        return redirect(url_for("nurses_page"))

def nurse_page():  # this will take parameter
    db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
    cursor = db.cursor()
    # select the nurse 
    #db.commit()
    cursor.close()
    #return render_template("nurse.html", nurse=nurse)
    return "success"

def filter_page():
    return render_template("filter.html")
def review_page():
    return render_template("review.html")
    
def signup_page():
    if request.method == "GET":
        values = {"name": "", "homename": "","city":"", "email":"","password":"",
        "type":"", "address":"", "tel":""
        }
        return render_template(
            "signup.html", values = values,
        )
    else:
        form_name = request.form["name"] 
        form_homename = request.form["homename"]
        form_city = request.form["city"]
        form_email = request.form["email"]
        form_password = request.form["password"]
        form_address = request.form["address"]
        form_tel = request.form["tel"]
        form_type = request.form["type"]
        
        name = str(form_name)
        homename = str(form_homename)
        city = str(form_city)
        email = str(form_email)
        password = str (form_password)
        address = str(form_address)
        type_ = str (form_type)
        tel = str(form_tel)

        hashed_password = hasher.hash(password)
    
        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()

        cursor.execute("DROP TABLE IF EXISTS Doctor")
        cursor.execute("DROP TABLE IF EXISTS Nursinghome")
        
        cursor.execute("CREATE TABLE Nursinghome(homeid INT AUTO_INCREMENT,name VARCHAR(40) NOT NULL,city VARCHAR(40) NOT NULL,type VARCHAR(40) NOT NULL,address VARCHAR(40) NOT NULL,tel VARCHAR(40) NOT NULL,PRIMARY KEY (homeid))")
        cursor.execute("CREATE TABLE Doctor(doctorid INT AUTO_INCREMENT,email VARCHAR(40) UNIQUE,name VARCHAR (40) NOT NULL ,password VARCHAR (64)  NOT NULL ,nursinghomeid INT,FOREIGN KEY (nursinghomeid)  REFERENCES Nursinghome(homeid) ON DELETE CASCADE ON UPDATE CASCADE,PRIMARY KEY (doctorid))")

        line1 = "INSERT INTO Nursinghome(name,city,type,address,tel) VALUES (%s,%s,%s,%s,%s)"
        data1 = (homename,city,type_,address,tel)
        cursor.execute(line1, data1)
        
        line2 = "INSERT INTO Doctor(name,email,password) VALUES (%s,%s,%s)"
        data2 = (name,email,hashed_password)
        cursor.execute(line2, data2)
        db.commit()
        cursor.close()
    return redirect(url_for("login_page"))


     
