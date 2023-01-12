from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user 
from wtforms import BooleanField, PasswordField, SelectField, SubmitField,  StringField, DateTimeField
from wtforms.validators import Email, EqualTo, DataRequired, InputRequired, Length, ValidationError, Optional, URL
from .models import *
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import UserMixin, login_user, login_required, logout_user, current_user


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class RegisterForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=4, max=15)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=4, max=15)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=200)])
    choices = [('client', 'Client'), ('fundi', 'Fundi')]
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class OrderForm(FlaskForm):
    
    title = StringField('Title', validators=[InputRequired(), Length(min=4, max=15)])
    description = StringField('Description', validators=[InputRequired(), Length(min=4, max=500)])
    locations = [('nyali', 'Nyali'), ('kongowea', 'Kongowea'), ('changamwe', 'Changamwe'), ('kisauni', 'Kisauni'), ('mvita', 'Mvita'), ('tudor', 'Tudor')]
    location = SelectField('Location', validators=[DataRequired()], choices=locations)
    services = [('plumbing', 'Plumbing'), ('electrical', 'Electrical'), ('carpentry', 'Carpentry'), ('painting', 'Painting'), ('tailoring', 'Tailoring'), ('barber', 'Barber'), ('casual', 'Just need some hands')]
    service = SelectField('Service Needed', validators=[DataRequired()], choices=services)
    image_link =  StringField('Image', default='', validators=[Optional(), URL()])
    #duration = SelectField('Due in', validators=[DataRequired()], choices=[('1', '1 hr'), ('2', '2 hrs'), ('4', '4 hrs'), ('6', '6 hrs'), ('8', '8 hrs'), ('12', '12 hrs')])
    prices = [('100-300', 'Ksh 100 - 300'), ('300-500', 'Ksh 300 - 500'), ('500-800', 'Ksh 500 - 800'), ('1000', 'Ksh 1000+') ]
    price_range = SelectField('Price Range', validators=[DataRequired()], choices=prices)
    submit = SubmitField('Submit')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')