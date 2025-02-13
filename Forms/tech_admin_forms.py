from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, DateField
from wtforms.validators import Email, InputRequired, Regexp, EqualTo, Optional


class Login_form(FlaskForm):
    username = EmailField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField(label="Login")

class Change_password_form(FlaskForm):
    username = EmailField(validators=[InputRequired()])
    old_password = PasswordField(validators=[InputRequired()])
    new_password = PasswordField(validators=[InputRequired(),Regexp(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', message="Should contain at least one uppercase letter, one special character one digit and should have minimum 8 characters in length")])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('new_password',message='Confirm new password: should match with new password')])
    submit = SubmitField("Change password")

class Schedule_movie_form(FlaskForm):
    movie_name = SelectField(validators=[InputRequired()])
    theater_name = SelectField(validators=[InputRequired()])
    start_date = DateField(validators=[InputRequired()])
    end_date = DateField(validators=[InputRequired()])
    submit = SubmitField(label="Schedule")

class Delete_schedule_form(FlaskForm):
    movie_name = SelectField(validators=[InputRequired()])
    theater_name = SelectField(validators=[InputRequired()])
    start_date = DateField(validators=[InputRequired()])
    submit = SubmitField(label="Delete")

class Filter_movie_form(Delete_schedule_form):
    movie_name = SelectField()
    theater_name = SelectField()
    start_date = DateField(validators=[Optional()])
    submit = SubmitField(label="Filter")
    