from flask import Flask, render_template,request,url_for,redirect,flash,session
import views
from flask_mysqldb import MySQL



app = Flask(__name__)
mysql = MySQL(app)


app.config["app"]=app
app.config["mysql"]=mysql

app.secret_key = "secret"

# heroku db:
app.config['MYSQL_HOST'] = "eu-cdbr-west-03.cleardb.net"
app.config['MYSQL_USER'] = "ba0e19c7c7c293"
app.config['MYSQL_PASSWORD'] = "0ecf3d8d"
app.config['MYSQL_DB'] = "heroku_6da1ba342772e3b"

#localhost:
#app.config['MYSQL_HOST'] = "localhost"
#app.config['MYSQL_USER'] = "root"
#app.config['MYSQL_PASSWORD'] = "1616"
#app.config['MYSQL_DB'] = "db_nursing"

app.add_url_rule("/", view_func=views.home)
app.add_url_rule("/signup", view_func=views.signup_page, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=views.logout_page)
app.add_url_rule("/filter", view_func=views.filter_page, methods=["GET", "POST"])
app.add_url_rule("/review", view_func=views.review_page, methods=["GET", "POST"])
app.add_url_rule("/profile", view_func=views.profile_page, methods=["GET", "POST"])
app.add_url_rule("/profile/edit", view_func=views.profile_edit_page, methods=["GET", "POST"])
app.add_url_rule("/nurse_edit", view_func=views.nurse_add_page, methods=["GET", "POST"]  )
app.add_url_rule("/nurses", view_func=views.nurses_page, methods=["GET", "POST"])
app.add_url_rule("/nurse/<int:nurseid>", view_func=views.nurse_page, methods=["GET", "POST"])
app.add_url_rule("/nurse/<int:nurseid>/edit", view_func=views.nurse_edit_page, methods=["GET", "POST"])

app.add_url_rule("/diseases", view_func=views.diseases_page, methods=["GET", "POST"])
app.add_url_rule("/disease/<int:diseaseid>", view_func=views.disease_page)
app.add_url_rule("/disease/<int:diseaseid>/edit", view_func=views.disease_edit_page, methods=["GET", "POST"])
app.add_url_rule("/disease_edit", view_func=views.disease_add_page, methods=["GET", "POST"]  )

app.add_url_rule("/residents", view_func=views.residents_page, methods=["GET", "POST"])
app.add_url_rule("/resident_edit", view_func=views.resident_add_page, methods=["GET", "POST"] )
app.add_url_rule("/resident/<int:residentid>", view_func=views.resident_page,methods=["GET", "POST"] )
app.add_url_rule("/resident/<int:residentid>/disease_add", view_func=views.resident_disease_page, methods=["GET", "POST"])
app.add_url_rule("/resident/<int:residentid>/edit", view_func=views.resident_edit_page, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True)  # for local
    #app.run() # for heroku deploy
