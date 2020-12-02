from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,SelectField
from wtforms.validators import EqualTo,DataRequired

class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    gender = SelectField(choices=[
        ("male","Male"),
        ("female","Female"),
        ("none","No Gender")
    ])
    mobile = StringField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
    birthday = DateField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    confirm = PasswordField(validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Register")