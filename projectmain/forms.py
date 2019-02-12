from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,DateTimeField,TextAreaField,SelectField,DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from projectmain.dbcode import state,district,city,cylinders,agent,User_reg,connection_type,booking,feedback



class RegistrationForm(FlaskForm):
    FirstName =StringField('FirstName',
                           validators=[DataRequired(), Length(min=2, max=20)])
    LastName =StringField('LastName')
   
    Gender = SelectField('Gender', choices = [('Male','Male'),('Female','Female')])
    PhoneNo =StringField('PhoneNo')
    Address = TextAreaField("Address")
    state = SelectField('state',choices=[('karnataka','karnataka'),('delhi','delhi'),('tamilnadu','tamilnadu'),('bihar','bihar'),('kerala','kerala')])
    district = SelectField('district',choices=[('udupi','udupi'),('mangalore','mangalore'),('bangalore','bangalore'),('belgum','belgum'),('kochi','kochi'),('chennai','chennai'),('kannur','kannur'),('hyderabad','hyderabad'),('agra','agra'),('saran','saran')])
    city = SelectField('city',choices=[('brahmavara','brahmavara'),('kundapura','kundapura'),('barkur','barkur'),('santekatte','santekatte'),('manipal','manipal'),('kadri','kadri'),('kavoor','kavoor'),('kottara','kottara'),('katil','katil'),('vaynad','vaynad'),('shabarimale','shabarimale'),('kottara','kottara'),('taj','taj'),('lacknow','lacknow')])
    connectionType = SelectField('connectionType', choices = [('domestic','domestic'),('comercial','comercial')])
    username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=20)])
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


class LoginForm(FlaskForm):
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember Me')
    submit = SubmitField('login')