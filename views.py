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
        #resident = Resident(form_name, form_age, form_gender)

        db = MySQLdb.connect(host="localhost", user="root", passwd="1616", db="db_nursing")
        cursor = db.cursor()
        #cursor.execute("INSERT INTO Resident(name, age, gender) VALUES (%s,%s,%s))
        cursor.execute("INSERT INTO Resident(name, age, gender) VALUES(%s,%s,%s)", (form_name,form_age,form_gender))
       #line = "INSERT INTO Resident(name, age, gender) VALUES (%s,%s,%s)"
        #cursor.execute(line,(form_name,form_age,form_gender))
        db.commit()
        cursor.close()
       # return redirect(url_for("resident_add_page"))
        return "success"

def residents_page():
    if request.method == "GET":
        return render_template("residents.html")
    else:
        return redirect(url_for("residents_page"))
