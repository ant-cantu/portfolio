from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class ContactForm(FlaskForm):
    name = StringField('Name:', validators=[
        DataRequired(message="You must enter your name."),
        Length(min=3, max=30, message="A minimum of 3 characters and max of 30 is allowed.")
    ])

    email = StringField('E-Mail:', validators=[
        DataRequired(message='Your must enter your email address, so I can reach you.'),
        Email(message='Must be a valid email.')
    ])

    message = TextAreaField('Message:', validators=[
        DataRequired(message='Message cannot be empty.'),
        Length(min=10, max=250, message='A minimum of 10 characters and max of 250 characters is allowed.')
    ])

    terms = BooleanField('accept', validators=[
        InputRequired(message='You must accept the terms to send me a message.')
    ])

    submit = SubmitField('Send')

    # Spam Honeypot
    honeypot = StringField('Leave this form empty', render_kw={"class": "honeypot"})