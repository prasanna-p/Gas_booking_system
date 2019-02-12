from flask import render_template,url_for,flash, redirect,request
from projectmain.forms import RegistrationForm, LoginForm
from projectmain import app,bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
from projectmain.dbcode import roles,state,district,city,cylinders,agent,User_reg,connection_type,booking,feedback


@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html',title="Home")


@app.route('/about')
def about():
    return render_template('about.html',title="about")


@app.route('/contact')
def contact():
    complaint = url_for('static',filename='pictures/complaints.png')
    contact = url_for('static',filename='pictures/contact.png')
    feedback = url_for('static',filename='pictures/feedback.png')
    return render_template('contact.html',title="contact",complaint=complaint,contact=contact,feedback=feedback)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        stname = state.query.filter_by(state_name=form.state.data).first()
        sid=stname.id
        dname = district.query.filter_by(dname=form.district.data).first()
        did=dname.did
        ctname = city.query.filter_by(cname=form.city.data).first()
        cid=ctname.cid
        cname = connection_type.query.filter_by(cname=form.connectionType.data).first()
        cttid=cname.ctid
        user = User_reg(fname=form.FirstName.data,lname=form.LastName.data,gender=form.Gender.data,phone_no=form.PhoneNo.data,adress=form.Address.data,sid=sid,did=did,cid=cid,ctid=cttid,username=form.username.data,email=form.email.data,password=hashed_pwd)
        roleadd = roles(email=form.email.data,password=hashed_pwd,role='consumer')
        db.session.add(user)
        db.session.add(roleadd)
        db.session.commit()
        flash(f'Your account has been created! now your able to login', 'success')
        return redirect(url_for('login'))
    return render_template('regestration.html',title='register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = roles.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful1. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/Alogin", methods=['GET', 'POST'])
def Alogin():
    form = LoginForm()
    if form.validate_on_submit():
        user = roles.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful1. Please check email and password', 'danger')
    return render_template('Alogin.html', title='Login', form=form)

@app.route("/Dlogin", methods=['GET', 'POST'])
def Dlogin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = roles.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful2. Please check username and password', 'danger')
    return render_template('dlogin.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('user_account.html',title='account',db=User_reg)

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html',title='admin')

@app.route('/distributor')
@login_required
def distributor():
    return render_template('distributor.html',title='distributor',db=agent)