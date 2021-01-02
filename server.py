from flask import Flask, render_template,request
import views
from flask_mysqldb import MySQLdb

def create_app():
    app = Flask(__name__)

    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home)
    app.add_url_rule("/signup", view_func=views.signup_page, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/filter", view_func=views.filter_page)
    app.add_url_rule("/review", view_func=views.review_page)

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
    app.add_url_rule("/resident/<int:residentid>", view_func=views.resident_page)
    app.add_url_rule("/resident/<int:residentid>/disease_add", view_func=views.resident_disease_page, methods=["GET", "POST"])
    app.add_url_rule("/resident/<int:residentid>/edit", view_func=views.resident_edit_page, methods=["GET", "POST"])
   
    
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)

