from flask import render_template,url_for,flash,redirect,request,jsonify,Blueprint
from projectmain.main.forms import(Homestatus,LoginForm,FeedBackForm)
from projectmain.dbcode import (state,district,cylinders,agent,roles,feedback)
from flask_login import login_user,current_user,login_required
from projectmain import bcrypt
from datetime import datetime
from projectmain import db


Main=Blueprint('Main',__name__)

db1=district
@Main.route('/')
@Main.route('/home',methods=['GET', 'POST'])
def home():
   form=Homestatus()
   form.state.choices = [(s.id, s.state_name) for s in state.query.all()]
   form.district.choices = [(d.did, d.dname) for d in db1.query.filter_by(sid=form.state.data).all()]
   form.agency_name.choices = [(a.aid, a.agency_name) for a in agent.query.filter_by(did=form.district.data).all()]
   cil=None
   age=None
   if form.validate_on_submit():
    cil = cylinders.query.filter_by(aid=form.agency_name.data).first()
    age=agent.query.filter_by(aid=form.agency_name.data).first()
   return render_template('home.html',title="Home",cily=cil,form=form,age=age)


@Main.route('/about')
def about():
    return render_template('about.html',title="about")


@Main.route('/contact')
def contact():
    complaint = url_for('static',filename='pictures/complaints.png')
    contact = url_for('static',filename='pictures/contact.png')
    feedback = url_for('static',filename='pictures/feedback.png')
    return render_template('contact.html',title="contact",complaint=complaint,contact=contact,feedback=feedback)


@Main.route('/Agent_contact',methods=['GET', 'POST'])
def Agent_contact():
   form=Homestatus()
   form.state.choices = [(s.id, s.state_name) for s in state.query.all()]
   form.district.choices = [(d.did, d.dname) for d in db1.query.filter_by(sid=form.state.data).all()]
   form.agency_name.choices = [(a.aid, a.agency_name) for a in agent.query.filter_by(did=form.district.data).all()]
   age=None
   if form.validate_on_submit():
    age=agent.query.filter_by(aid=form.agency_name.data).first()
   return render_template('agent_contact.html',title="Home",form=form,age=age)



@Main.route('/district/<st>')
def district(st):
    dist = db1.query.filter_by(sid=int(st)).all()

    distArray = []

    for d in dist:
        distObj = {}
        distObj['id'] =d.did
        distObj['name'] = d.dname
        distArray.append(distObj)

    return jsonify({'dist' : distArray})


@Main.route('/agency_name/<di>')
def agency_name(di):
    agents = agent.query.filter_by(did=int(di)).all()

    ageArray = []

    for age in agents:
        ageObj = {}
        ageObj['id'] = age.aid
        ageObj['name'] = age.agency_name
        ageArray.append(ageObj)

    return jsonify({'agents' : ageArray})

@Main.route("/mlogin", methods=['GET', 'POST'])
def mlogin():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = roles.query.filter_by(email=form.email.data).first()
        if user and user.role=='admin' and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Main.home'))
        if user and user.role=='agent' and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Main.home'))
        if user and user.role=='consumer' and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Main.home'))
        else:
            flash('Login Unsuccessfull. Please check email and password', 'danger')
    return render_template('mlogin.html', title='Login', form=form)


@Main.route("/MFeedBack",methods=['GET','POST'])
def MFeedBack():
    form =  FeedBackForm()
    if form.validate_on_submit():
        messege = feedback(sub=form.subject.data,description=form.description.data,
                    sdate=datetime.utcnow(),role='user')
        db.session.add(messege)
        db.session.commit()
        flash('Your feed Back has been submitted successfully','info')
        return redirect(url_for('Main.MFeedBack'))
    return render_template('mfeedback.html',title='feedbck',form=form)