from flask import render_template,url_for,flash, redirect,request,jsonify,Blueprint,abort
from projectmain.main.forms import (LoginForm,UpdateForm,RequestResetForm,ResetPasswordForm,FeedBackForm)
from projectmain.consumer.forms import RegistrationForm
from projectmain import bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
from projectmain.dbcode import roles,User_reg,state,district,city,agent,connection_type,booking,feedback
from projectmain.main.util import save_picture,send_reset_email,send_email
from datetime import datetime



Consumer = Blueprint('Consumer',__name__)

db1=district
db2=city

@Consumer.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form = RegistrationForm()
    form.state.choices =[(s.id, s.state_name) for s in state.query.all()]
    form.district.choices = [(d.did, d.dname) for d in db1.query.filter_by(sid=form.state.data).all()]
    form.city.choices = [(c.cid, c.cname) for c in db2.query.filter_by(did=form.district.data).all()]
    form.agency_name.choices = [(a.aid, a.agency_name) for a in agent.query.filter_by(did=form.district.data).all()]
    form.connectionType.choices =[(c.ctid, c.cname) for c in 
              connection_type.query.filter(connection_type.agents.any(aid=form.agency_name.data)).all()]    
    if form.validate_on_submit():
        hashed_pwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User_reg(fname=form.FirstName.data,lname=form.LastName.data,gender=form.Gender.data,phone_no=form.PhoneNo.data,adress=form.Address.data,sid=form.state.data,did=form.district.data,cid=form.city.data,aid=form.agency_name.data,ctid=form.connectionType.data,username=form.username.data,email=form.email.data,password=hashed_pwd)
        roleadd = roles(email=form.email.data,password=hashed_pwd,role='consumer')
        db.session.add(user)
        db.session.add(roleadd)
        db.session.commit()
        roleadd.uid=user.id
        db.session.commit()
        flash(f'Your account has been created! now your able to login', 'success')
        return redirect(url_for('Consumer.login'))
    return render_template('regestration.html',title='register', form=form)


@Consumer.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = roles.query.filter_by(email=form.email.data).first()
        if user and user.role=='consumer' and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Main.home'))
        else:
            flash('Login Unsuccessfull. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@Consumer.route('/account')
@login_required
def account():
    if current_user.is_authenticated and current_user.role=='consumer':
        pass
    else:
        abort(403)
    return render_template('user_account.html',title='account',db=User_reg)

@Consumer.route('/profile',methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_authenticated and current_user.role=='consumer':
        pass
    else:
        abort(403)
    form = UpdateForm()
    user = User_reg.query.filter_by(email=current_user.email).first()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.email = form.email.data
        user.username = form.username.data
        user.phone_no = form.PhoneNo.data
        user.adress = form.Address.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('Consumer.profile'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = current_user.email
        form.PhoneNo.data = user.phone_no
        form.Address.data = user.adress
    img = url_for('static',filename='pictures/'+user.image_file)
    return render_template('user/profile.html',db=User_reg,img=img,form=form)
    
@Consumer.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User_reg.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('Consumer.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@Consumer.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    user = User_reg.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('Consumer.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        role=roles.query.filter_by(email=user.email).first()
        role.password = user.password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('Consumer.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@Consumer.route("/Uconnection",methods=['GET', 'POST'])
@login_required
def Uconnection():
    if current_user.is_authenticated and current_user.role=='consumer':
        pass
    else:
        abort(403)
    user = User_reg.query.filter_by(id=current_user.uid).first()
    ctype = connection_type.query.filter_by(ctid=user.ctid).first()
    agents = agent.query.filter_by(aid=user.aid).first()
    return render_template('Uconnection.html',title='connection details',user=user,
                            ctype=ctype,agents=agents)


@Consumer.route("/Uconnection/<int:uid>/<int:aid>/submit",methods=['GET','POST'])
@login_required
def Booking(uid,aid):
    book = booking(bdate=datetime.utcnow(),uid=uid,aid=aid,status='Not Delivered')
    db.session.add(book)
    db.session.commit()
    flash('Your Gas booking request has been submitted', 'info')
    user = User_reg.query.filter_by(id=uid).first()
    age = agent.query.filter_by(aid=aid).first()
    send_email(user,age)
    return redirect(url_for('Consumer.Uconnection'))


@Consumer.route("/Bstatus",methods=['GET','POST'])
@login_required
def Bstatus():
    if current_user.is_authenticated and current_user.role=='consumer':
        pass
    else:
        abort(403)
    book = booking.query.filter_by(uid=current_user.uid).all()
    return render_template('Bstatus.html',title='booking status',book=book,agent=agent)



@Consumer.route("/FeedBack",methods=['GET','POST'])
@login_required
def FeedBack():
    if current_user.is_authenticated and current_user.role=='consumer':
        pass
    else:
        abort(403)
    form =  FeedBackForm()
    if form.validate_on_submit():
        messege = feedback(sub=form.subject.data,description=form.description.data,
                    sdate=datetime.utcnow(),uid=current_user.uid,role='consumer')
        db.session.add(messege)
        db.session.commit()
        flash('Your feed Back has been submitted successfully','success')
        return redirect(url_for('Consumer.FeedBack'))
    return render_template('cfeedback.html',title='feedbck',form=form,legend="consumer feedback")


@Consumer.route("/Complaint",methods=['GET','POST'])
@login_required
def Complaint():
    if current_user.is_authenticated and current_user.role=='consumer':
        pass
    else:
        abort(403)
    form =  FeedBackForm()
    if form.validate_on_submit():
        messege = feedback(sub=form.subject.data,description=form.description.data,
                    sdate=datetime.utcnow(),uid=current_user.uid,role='complaint')
        db.session.add(messege)
        db.session.commit()
        flash('Your complaint has been recieved','success')
        return redirect(url_for('Consumer.Complaint'))
    return render_template('complaint.html',title='complaint',form=form)