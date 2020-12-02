from flask import Blueprint,render_template,redirect,url_for
from myproject.models import Product
from flask_login import logout_user,login_required

index_blueprint = Blueprint("index",__name__,template_folder="templates/index")

@index_blueprint.route("/")
def index():
    product_list = Product.query.all()
    print(product_list)
    return render_template("index.html",product_list=product_list)

@index_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index.index"))