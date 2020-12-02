from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,SelectField,FileField,TextAreaField,FloatField
from wtforms.validators import DataRequired
from myproject.models import Category


class AdminLoginForm(FlaskForm):
    email = StringField()
    password = PasswordField()
    submit = SubmitField()

class AddProductForm(FlaskForm):
    name = StringField()
    description = TextAreaField()
    category = SelectField()
    expireDate = StringField()
    stock = StringField()
    img = FileField()
    manufacturer = StringField()
    price = FloatField()
    minBid = FloatField()
    submit = SubmitField()

    def __init__(self):
        super().__init__()
        self.category.choices = [(cat.name,cat.name) for cat in Category.query.all()]
    
class AddCategoryFrom(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField("ADD NEW CATEGORY")