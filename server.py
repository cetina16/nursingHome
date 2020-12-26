from flask import Flask, render_template,request
import views
from disease import Disease
from database import Database
from flask_login import LoginManager
from user import get_user
from flask_mysqldb import MySQLdb

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)

    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home)

    db = MySQLdb.connect(host = "localhost", user ="root", passwd = "1616")

    app.add_url_rule( "/diseases", view_func=views.diseases_page, methods=["GET", "POST"])
    app.add_url_rule( "/residents", view_func=views.residents_page, methods=["GET", "POST"])
    app.add_url_rule("/resident_edit", view_func=views.resident_add_page, methods=["GET", "POST"]  )
    app.add_url_rule("/disease_edit", view_func=views.disease_add_page, methods=["GET", "POST"]  )
    app.add_url_rule("/diseases/<int:disease_key>", view_func=views.disease_page)
    app.add_url_rule(
        "/diseases/<int:disease_key>/edit",
        view_func=views.disease_edit_page,
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/login", view_func=views.login_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/logout", view_func=views.logout_page)
 
    lm.init_app(app)
    lm.login_view = "login_page" 

    db = Database()
    db.add_disease(Disease("Diabetes", risklevel=3,period=3))
    db.add_disease(Disease("Covid-19", risklevel=4))
    app.config["db"] = db
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)

