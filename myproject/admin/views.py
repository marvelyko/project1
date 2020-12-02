from flask import Blueprint,render_template,redirect,url_for,flash
import flask
from flask_login import current_user,login_user,logout_user,login_required
from myproject.models import User,Admin,Product,Category
from myproject.admin.forms import AdminLoginForm,AddProductForm,AddCategoryFrom
from myproject import app,login_manager,db,basedir
from functools import wraps
from werkzeug.utils import secure_filename
import os

admin_blueprint = Blueprint("admin",__name__,template_folder="templates/admin")

@admin_blueprint.route("/",methods=["GET","POST"])
def index():
    form = AdminLoginForm()
    if not current_user.is_anonymous:
        if Admin.query.filter_by(user_id=current_user.id).first():
            return render_template("admin-index.html")
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data) and Admin.query.filter_by(user_id=user.id).first():
                login_user(user)
                return redirect(url_for("admin.index"))
            else:
                flash("Wrong credentials")
    return render_template("admin-login.html",form=form)


def admin_required(func):
    @wraps(func)
    @login_required
    def decorated_view(*args, **kwargs):
        if not Admin.query.filter_by(user_id=current_user.id).first():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

@admin_blueprint.route("/products",methods=["GET","POST"])
@admin_required
def manage_products():
    product_list = Product.query.all()
    category_list = Category.query.all()
    add_category_form = AddCategoryFrom()
    if add_category_form.validate_on_submit():
        name = add_category_form.name.data
        category = Category(name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("admin.manage_products"))
    return render_template("admin-products.html",product_list=product_list,category_list=category_list,category_form = add_category_form)

@admin_blueprint.route("/add-product",methods=["GET","POST"])
@admin_required
def add_products():
    form = AddProductForm()
    if form.validate_on_submit():
        product = Product(form.name.data,"Bog.ge",form.stock.data,100)
        path = os.path.join(basedir,"static","uploads",form.img.data.filename)
        form.img.data.save(path)
        product.image = os.path.join("static","uploads",form.img.data.filename)
        product.sold_quantity = 0
        product.expire_data = form.expireDate.data
        product.category = Category.query.filter_by(name=form.category.data).id
        db.session.add(product)
        db.session.commit()
    return render_template("add-product.html",form=form)

@admin_blueprint.route("/delete-product/<int:id>",methods=["GET","POST"])
@admin_required
def delete_product(id):
    if flask.request.method == "GET":
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("admin.manage_products"))

@admin_blueprint.route("/delete-products",methods=["GET","POST"])
@admin_required
def delete_products():
    if flask.request.method == "POST":
        for product_id in flask.request.form.getlist("product"):
            product = Product.query.get(int(product_id))
            db.session.delete(product)
        db.session.commit()
        return redirect(url_for("admin.manage_products"))

@admin_blueprint.route("/logout")
@admin_required
def logout():
    logout_user()
    return redirect(url_for("admin.index"))

@admin_blueprint.route("/delete-category/<name>")
@admin_required
def delete_category(name):
    category = Category.query.filter_by(name=name).first()
    if category:
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for('admin.manage_products'))