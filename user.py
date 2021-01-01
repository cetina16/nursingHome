from flask import current_app

class User:
    def __init__(self, email, password,name,homeid):
        self.email = email
        self.password = password
        self.name = name
        self.homeid = homeid
        self.active = True

    def get_id(self):
        return self.homeid

    @property
    def is_active(self):
        return self.active


#def get_user(user_id):
   # password = current_app.config["PASSWORDS"].get(user_id)
    #name = current_app.config["USER_NAMES"].get(user_id)
    #user = User(user_id, password,name) if password else None
    #if user is not None:
    #    user.is_admin = user.email in current_app.config["USERS"]
    #return 
    
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