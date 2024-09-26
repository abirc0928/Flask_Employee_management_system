from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange,  Email, EqualTo, ValidationError
from models import User


class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    salary = FloatField('Salary', validators=[DataRequired(), NumberRange(min=0)])
    
    # Dropdown for designation
    designation = SelectField(
        'Designation', 
        choices=[
            ('manager', 'Manager'), 
            ('developer', 'Developer'), 
            ('designer', 'Designer'), 
            ('analyst', 'Analyst')
        ],
        validators=[DataRequired()]
    )
    short_description = TextAreaField('Short Description', validators=[Length(max=500)])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use.')
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')