from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from Jurzo.models import User

class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4,max=30)])
    password = PasswordField("password",validators=[DataRequired(), Length(min=6,max=18)])
    confirm_password = PasswordField("Confirm password",validators=[DataRequired(),EqualTo('password')])
    email = StringField("Email id",validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user= User.query.filter_by( email = email.data).first()
        if user:
            raise ValidationError('This Email already exists. Please choose a diffrent one')

    def validate_username(self, username):
        user= User.query.filter_by( username = username.data).first()
        if user:
            raise ValidationError('This Username already exists. Please choose a diffrent one')



class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=4,max=30)])
    password = PasswordField('password',validators=[DataRequired(),Length(min=6,max=18)])
    remember_me = BooleanField()
    submit=SubmitField('Log In')


class PageForm(FlaskForm):
    name=StringField("Your Name",validators=[DataRequired()])
    pet_name= StringField('My friends call me',validators=[DataRequired()])
    phone_num= StringField('Tring Tring....',validators=[DataRequired()])
    address=TextAreaField('Home sweet Home...' , validators=[DataRequired()])
    mail = StringField('My .com adress....' ,validators=[DataRequired()])
    birthday = StringField('Wish me on..(dd/mm/yyyy) ' , validators = [DataRequired()])
    nick_name = StringField("if you'd give me a nickname...")
    Quote = StringField("Quotable Quote..." , validators=[DataRequired()])
    Songs = StringField('A song for me...?')
    likes = TextAreaField("A thing you like in me..")
    hates = TextAreaField("A thing you hate in me....")
    what_us = TextAreaField("What am I to you...?", validators=[DataRequired()])
    lastd = TextAreaField("If today was my last day, and I'm With you, What should we do?")
    submit=SubmitField("Done")


class RequestResetForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired()])
    submit= SubmitField('Request Reset Password')

    def validate_email(self,email):

        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError('No account linked to that email.Please SignUp first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField("password",validators=[DataRequired(), Length(min=6,max=18)])
    confirm_password = PasswordField("Confirm password",validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Reset Password')


