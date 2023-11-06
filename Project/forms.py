from flask_wtf import FlaskForm
from flask_login import current_user
from flask_login import login_user,current_user,logout_user, login_required,UserMixin
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo , ValidationError
#from app import User

class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname',validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    """def validate_username(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email-ID is already used')
"""

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DataForm(FlaskForm):
    pregnancies=StringField('Pregnancies',validators=[DataRequired()])
    glucose=StringField('Glucose',validators=[DataRequired()])
    bloodpressure=StringField('BloopPressure',validators=[DataRequired()])
    skinthickness=StringField('SkinThickness',validators=[DataRequired()])
    insulin=StringField('Insulin',validators=[DataRequired()])
    bmi=StringField('BMI',validators=[DataRequired()])
    diabetespedigreefunction=StringField('DiabetesPedigreeFunction',validators=[DataRequired()])
    age=StringField('Age',validators=[DataRequired()])
    submit=SubmitField('Predict')