from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, DateField
from wtforms.validators import Email, InputRequired, Regexp, EqualTo


class Login_form(FlaskForm):
    username = EmailField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(),Regexp(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')])
    submit = SubmitField(label="Login")

class Change_password_form(FlaskForm):
    username = EmailField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(),Regexp(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')])
    confirm_password = PasswordField(validators=[InputRequired(),Regexp(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'), EqualTo(password)])
    submit = SubmitField()

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
    submit = SubmitField(label="Filter")