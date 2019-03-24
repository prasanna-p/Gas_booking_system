from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,BooleanField,
                        TextAreaField,SelectField,SelectMultipleField,IntegerField)

from wtforms.validators import (DataRequired, Length, Email, 
                                    EqualTo,ValidationError)

from projectmain.dbcode import state,district,city,cylinders,agent,User_reg,connection_type
db1=district
db2=city
db3=state


class stateForm(FlaskForm):
    st_name = StringField("State Name",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('update')

    def validate_st_name(self,st_name):
        st = db3.query.filter_by(state_name=st_name.data).first()
        if st:
            raise ValidationError('That State Name  is taken. Please choose a different one.')

class UstateForm(FlaskForm):
    st_name = StringField("State Name",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('update')

class districtForm(FlaskForm):
    st_name = SelectField('state',coerce=int,choices=[])
    district = StringField("district Name",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('update')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        d = db1.query.filter_by(dname=self.district.data,sid=self.st_name.data).first()
        if d:
            self.district.errors.append('District Name is already taken')
            return False

        return True

class UdistrictForm(FlaskForm):
    st_name = SelectField('state',coerce=int,choices=[])
    district = StringField("district Name",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('update')


class cityForm(FlaskForm):
    state = SelectField('state',coerce=int,choices=[])
    district = SelectField('district',coerce=int,choices=[])
    city = StringField("city Name",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('update')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
 
        d = db2.query.filter_by(cname=self.city.data,did=self.district.data).first()
        if d:
            self.city.errors.append('That City Name is taken. Please choose a different one.')
            return False

        return True
            

class UcityForm(FlaskForm):
    state = SelectField('state',coerce=int,choices=[])
    district = SelectField('district',coerce=int,choices=[])
    city = StringField("city Name",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField('update')

class cilyForm(FlaskForm):
    state = SelectField('state',coerce=int,choices=[])
    district = SelectField('district',coerce=int,choices=[])    
    agency_name = SelectField('agency_name',coerce=int,choices=[])
    tcylinder = IntegerField('total cylinders',validators=[DataRequired()])
    acylinder = IntegerField('availabel cylinders',validators=[DataRequired()])
    submit = SubmitField('submit')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if self.acylinder.data>self.tcylinder.data:
            self.acylinder.errors.append('availabel cylinder is greater than total')
            return False

        return True

class UcilyForm(FlaskForm):
    state = SelectField('state',coerce=int,choices=[])
    district = SelectField('district',coerce=int,choices=[])    
    agency_name = SelectField('agency_name',coerce=int,choices=[])
    tcylinder = IntegerField('total cylinders',validators=[DataRequired()])
    acylinder = IntegerField('availabel cylinders',validators=[DataRequired()])
    submit = SubmitField('submit')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if self.acylinder.data>self.tcylinder.data:
            self.acylinder.errors.append('availabel cylinder is greater than total')
            return False

        return True


class ConForm(FlaskForm):
    connectionType = StringField('Connection Name',validators=[DataRequired()] )
    rfillcharge = IntegerField('Refill Charge',validators=[DataRequired()])
    ncharge = IntegerField('New Connection Charge',validators=[DataRequired()])
    submit = SubmitField('submit')

class dRegistrationForm(FlaskForm):
    FirstName =StringField('FirstName',
                           validators=[DataRequired(), Length(min=2, max=20)])
    LastName =StringField('LastName')
   
    Gender = SelectField('Gender', choices = [('Male','Male'),('Female','Female')])
    PhoneNo =StringField('PhoneNo')
    Address = TextAreaField("Address")
    state = SelectField('state',coerce=int,choices=[])    
    district = SelectField('district',choices=[],coerce=int)
    city = SelectField('city',choices=[],coerce=int)
    agency_name = StringField('agency_name',
                        validators=[DataRequired(),Length(max=50)])
    connectionType = SelectMultipleField('connectionType', coerce=int,choices =[])
    username = StringField('username',
                        validators=[DataRequired()])
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = agent.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self,email):
        user = agent.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

