from flask import render_template,url_for,flash, redirect,request,Blueprint,abort
from projectmain.main.forms import (LoginForm,UpdateForm,RequestResetForm,ResetPasswordForm,FeedBackForm)
from projectmain import bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
from projectmain.dbcode import roles,agent,booking,User_reg,city,connection_type,feedback
from projectmain.main.util import save_picture,dsend_reset_email,send_conformation_email
from datetime import datetime


Agent = Blueprint('Agent',__name__)

@Agent.route('/distributor')
@login_required
def distributor():
    if current_user.is_authenticated and current_user.role=='agent':
        pass
    else:
        abort(403)
    return render_template('distributor.html',title='distributor',db=agent)


@Agent.route("/Dlogin", methods=['GET', 'POST'])
def Dlogin():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = roles.query.filter_by(email=form.email.data).first()
        if user and user.role=='agent' and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Main.home'))
        else:
            flash('Login Unsuccessfull. Please check username and password', 'danger')
    return render_template('dlogin.html', title='Login', form=form)


@Agent.route('/dprofile',methods=['GET', 'POST'])
@login_required
def dprofile():
    if current_user.is_authenticated and current_user.role=='agent':
        pass
    else:
        abort(403)
    form = UpdateForm()
    user = agent.query.filter_by(email=current_user.email).first()
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
        return redirect(url_for('Agent.dprofile'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = current_user.email
        form.PhoneNo.data = user.phone_no
        form.Address.data = user.adress
    img = url_for('static',filename='pictures/'+user.image_file)
    return render_template('agent/dprofile.html',db=agent,img=img,form=form)


@Agent.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Main.home'))

@Agent.route("/dreset_password", methods=['GET', 'POST'])
def dreset_request():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = agent.query.filter_by(email=form.email.data).first()
        dsend_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('Agent.Dlogin'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@Agent.route("/dreset_password/<token>", methods=['GET', 'POST'])
def dreset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    user = agent.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('Agent.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        role=roles.query.filter_by(email=user.email).first()
        role.password = user.password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('Agent.Dlogin'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@Agent.route("/brequest", methods=['GET', 'POST'])
def brequest():
    if current_user.is_authenticated and current_user.role=='agent':
        pass
    else:
        abort(403)
    book = booking.query.filter_by(aid=current_user.aid,status='Not Delivered').all()
    return render_template('book.html',title='booking report',book=book,user=User_reg)

@Agent.route("/brequest/<int:bid>/Brupdate",methods=['GET','POST'])
@login_required
def Brupdate(bid):
    if current_user.is_authenticated and current_user.role=='agent':
        pass
    else:
        abort(403)
    book = booking.query.filter_by(bid=bid).first()
    book.ddate=datetime.utcnow()
    book.status = 'Delivered'
    db.session.commit()
    user = User_reg.query.filter_by(id=book.uid).first()
    age = agent.query.filter_by(aid=book.aid).first()
    send_conformation_email(user,age)
    return redirect(url_for('Agent.brequest'))

@Agent.route("/Dcreport",methods=['GET','POST'])
@login_required
def Dcreport():
    if current_user.is_authenticated and current_user.role=='agent':
        pass
    else:
        abort(403)
    users=User_reg.query.filter_by(aid=current_user.aid).all()
    return render_template('dcreport.html',title='customer report',users=users,city=city,ctype=connection_type)

@Agent.route("/AgentFeedBack",methods=['GET','POST'])
@login_required
def AgentFeedBack():
    if current_user.is_authenticated and current_user.role=='agent':
        pass
    else:
        abort(403)
    form =  FeedBackForm()
    if form.validate_on_submit():
        messege = feedback(sub=form.subject.data,description=form.description.data,
                    sdate=datetime.utcnow(),aid=current_user.aid,role='agent')
        db.session.add(messege)
        db.session.commit()
        flash('Your feed Back has been submitted successfully','success')
        return redirect(url_for('Agent.AgentFeedBack'))
    return render_template('afeedback.html',form=form,title='feedbck',legend='distributor feed back')