from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PageForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    pet_name = StringField('My friends call me', validators=[DataRequired()])
    phone_num = StringField('Tring Tring....', validators=[DataRequired()])
    address = TextAreaField('Home sweet Home...', validators=[DataRequired()])
    mail = StringField('My .com adress....', validators=[DataRequired()])
    birthday = StringField('Wish me on..(dd/mm/yyyy) ',
                           validators=[DataRequired()])
    nick_name = StringField("if you'd give me a nickname...")
    Quote = StringField("Quotable Quote...", validators=[DataRequired()])
    Songs = StringField('A song for me...?')
    likes = TextAreaField("A thing you like in me..")
    hates = TextAreaField("A thing you hate in me....")
    what_us = TextAreaField("What am I to you...?",
                            validators=[DataRequired()])
    lastd = TextAreaField(
        "If today was my last day, and I'm With you, What should we do?")
    submit = SubmitField("Done")
