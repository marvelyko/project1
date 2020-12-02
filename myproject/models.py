from myproject import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    manufacturer = db.Column(db.String)
    quantity = db.Column(db.Float)
    sku = db.Column(db.Float)
    min_Bid = db.Column(db.Float)
    image = db.Column(db.String)
    description = db.Column(db.String)
    sold_quantity = db.Column(db.Float)
    rating = db.Column(db.Float)
    comments = db.Column(db.String)
    category = db.relationship("Category",backref="product",lazy="dynamic")
    #admins = db.relationship('Admin',backref='admins')
    consultant = db.Column(db.String)
    tags = db.Column(db.String)
    shipping_price = db.Column(db.Float)
    location = db.Column(db.String)
    price=db.Column(db.Float)
    expire_data=db.Column(db.String)


    # file = db.relationship('File', backref='users')

    def __init__(self, name, manufacturer, quantity, cost):
        self.name = name
        self.manufacturer = manufacturer
        self.quantity = quantity
        self.cost=cost
        #self.sku =f"{self.name[0]}_{self.name[0]}_{self.name[0]}"

class Consultant(db.Model):
    __tablename__="consultants"
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

class User(db.Model,UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    birth_date = db.Column(db.DATE)
    phone = db.Column(db.String)
    bid = db.Column(db.String)
    bonus_points = db.Column(db.Integer)
    gender = db.Column(db.String)
    address = db.Column(db.String)
    admin = db.relationship("Admin",backref="users")

    # file = db.relationship('File', backref='users')

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password,password)

class Coupon(db.Model):
    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = db.Column(db.String)
    discount = db.Column(db.Float)

    def __init__(self, product, discount):
        self.product = product
        self.discount = discount


class Bid(db.Model):
    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = db.Column(db.String)
    quantity = db.Column(db.Float)

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    user = db.relationship("User",backref="admins")

    def __init__(self, user_id):
        self.user_id = user_id

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True)
    product_id = db.Column(db.Integer,db.ForeignKey("products.id"))

    def __init__(self,name):
        self.name = name