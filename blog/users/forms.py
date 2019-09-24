from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from blog.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2, max=20)]) 
        # data required meaning can't be empty
        # length of text
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):  
        user = User.objects.filter(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another')

    def validate_username (self, username):  
        user = User.objects.filter(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another')

class LoginForm(FlaskForm): 
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
        validators=[DataRequired()]) 
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2, max=20)]) 
        # data required meaning can't be empty
        # length of text
    email = StringField('Email',
        validators=[DataRequired(), Email()]) 
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):  
        if email.data != current_user.email: 
            raise ValidationError('Email can\'t not change')   

    def validate_username (self, username):  
        if username.data != current_user.username:
            user = User.objects.filter(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')
 
    def validate_email(self, email):  
        user = User.objects.filter(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
 