from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,TextAreaField,SelectField,
                    IntegerField)
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from projectmain.dbcode import User_reg


class RegistrationForm(FlaskForm):
    FirstName =StringField('FirstName',
                           validators=[DataRequired(), Length(min=2, max=20)])
    LastName =StringField('LastName')
   
    Gender = SelectField('Gender', choices = [('Male','Male'),('Female','Female')])
    PhoneNo =StringField('PhoneNo')
    Address = TextAreaField("Address")
    state = SelectField('state',coerce=int,choices=[])
    district = SelectField('district',choices=[], coerce=int)    
    city = SelectField('city',choices=[], coerce=int)
    agency_name = SelectField('agency_name',coerce=int, choices = [])
    connectionType = SelectField('connectionType',coerce=int, choices = [])
    username = StringField('username', 
                        validators=[DataRequired()])
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User_reg.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self,email):
        user = User_reg.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LocationTransferForm(FlaskForm):
    state = SelectField('state',coerce=int,choices=[])
    district = SelectField('district',choices=[], coerce=int)  
    city = SelectField('city',choices=[], coerce=int)
    agency_name = SelectField('agency_name',coerce=int, choices = [])
    connectionType = SelectField('connectionType',coerce=int, choices = [])
    reason = TextAreaField("transfer reaon")
    submit = SubmitField('Submit')
