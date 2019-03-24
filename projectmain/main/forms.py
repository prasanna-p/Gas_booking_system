from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField,BooleanField,
                        TextAreaField,SelectField)
from wtforms.validators import (DataRequired, Length, Email, EqualTo,
                                ValidationError)
from projectmain.dbcode import (agent,User_reg,roles)




class LoginForm(FlaskForm):
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember Me')
    submit = SubmitField('login')

class UpdateForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    PhoneNo =StringField('PhoneNo')
    
    Address = TextAreaField("Address")
    
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    picture = FileField('update profile picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('update')

    def validate_email(self,email):
        if email.data!=current_user.email:
             user = roles.query.filter_by(email=email.data).first()
             if user:
                raise ValidationError('That email is taken. Please choose a different one.')
    def validate_username(self,username):
        if current_user.role=='consumer':
            user = User_reg.query.filter_by(email=current_user.email).first()
            if username.data!=user.username:
                user1 = User_reg.query.filter_by(username=username.data).first()
                if user1:
                    raise ValidationError('That username is taken. Please choose a different one.')
        if current_user.role=='agent':
            user = agent.query.filter_by(email=current_user.email).first()
            if username.data!=user.username:
                user1 = agent.query.filter_by(username=username.data).first()
                if user1:
                    raise ValidationError('That username is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = roles.query.filter_by(email=email.data).first()        
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class Homestatus(FlaskForm):
    state = SelectField('state',coerce=int,choices=[])
    district = SelectField('district',coerce=int,choices=[])
    agency_name = SelectField('agency_name',coerce=int,choices=[])
    submit = SubmitField('Check for status')

class FeedBackForm(FlaskForm):
    subject=StringField('subject',validators=[DataRequired()])
    description = TextAreaField('description',validators=[DataRequired()])
    submit = SubmitField('submit')