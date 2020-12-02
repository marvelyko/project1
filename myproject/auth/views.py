from flask import Blueprint,render_template,flash
from myproject.auth.forms import RegisterForm
from myproject.models import User
from myproject import db


auth_blueprint = Blueprint("auth",__name__,template_folder="templates/auth")

@auth_blueprint.route("/register",methods=["GET","POST"])
def login():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data
        gender = form.gender.data
        mobile = form.mobile.data
        address = form.address.data
        birthday = form.birthday.data
        if User.query.filter_by(email=email).first():
            flash("Such user already exists")
            return render_template("login.html",form=form)
        else:
            user = User(email,password)
            user.name = name+" "+surname
            user.birth_date = birthday
            user.phone = mobile
            user.address = address
            user.gender = gender
            db.session.add(user)
            db.session.commit()

            
    return render_template("login.html",form=form)

@auth_blueprint.route("/success")
def success():
    return render_template("success.html")