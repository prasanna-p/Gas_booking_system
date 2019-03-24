from flask import render_template,url_for,flash, redirect,request,jsonify,Blueprint,abort
from projectmain.admin.forms import (dRegistrationForm,cilyForm,
                                    ConForm,stateForm,UstateForm,districtForm,
                                    cityForm,UdistrictForm,UcityForm,UcilyForm)
from projectmain.main.forms import (LoginForm)
from projectmain import bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
from projectmain.dbcode import (roles,state,district,city,cylinders,agent,
                                User_reg,connection_type,ctype,feedback)

from projectmain.errors.handlers import error_403

Admin = Blueprint('Admin',__name__)



db1=district
db2=city
db3=connection_type
@Admin.route('/st',methods=['GET', 'POST'])
@login_required
def st():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    form=stateForm()
    if form.validate_on_submit():
        stname = state(state_name=form.st_name.data)
        db.session.add(stname)
        db.session.commit()
    st=state.query.all()
    return render_template('state.html',title="state",st=st,form=form,legend='Add State')

@Admin.route("/st/<int:sid>/update", methods=['GET', 'POST'])
@login_required
def update_state(sid):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    st = state.query.get_or_404(sid)
    form = UstateForm()
    if form.validate_on_submit():
        st.state_name = form.st_name.data
        db.session.commit()
        flash('state name has been updated!', 'success')
        return redirect(url_for('Admin.st'))
    elif request.method == 'GET':
        form.st_name.data = st.state_name
    st=state.query.all()
    return render_template('state.html', title='Update state',
                           form=form,st=st,legend='Update State')


@Admin.route("/st/<int:sid>/delete", methods=['GET', 'POST'])
@login_required
def delete_state(sid):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    stat = state.query.get_or_404(sid)
    db.session.delete(stat)
    db.session.commit()
    flash('state has been removed!', 'success')
    return redirect(url_for('Admin.st'))



@Admin.route('/dist',methods=['GET', 'POST'])
@login_required
def dist():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    form=districtForm()
    form.st_name.choices=[(s.id, s.state_name) for s in state.query.all()]
    if form.validate_on_submit():
        dis = db1(dname=form.district.data,sid=form.st_name.data)
        db.session.add(dis)
        db.session.commit()
    dt=db1.query.all()
    return render_template('district.html',title="district",dt=dt,form=form,state=state,legend='Add district')

@Admin.route("/dist/<int:did>/update", methods=['GET', 'POST'])
@login_required
def update_dist(did):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    dt = db1.query.get_or_404(did)
    form = UdistrictForm()
    form.st_name.choices=[(s.id, s.state_name) for s in state.query.all()]
    if form.validate_on_submit():
        dt.dname = form.district.data
        dt.sid=form.st_name.data
        db.session.commit()
        flash('district name has been updated!', 'success')
        return redirect(url_for('Admin.dist'))
    elif request.method == 'GET':
        form.st_name.data = dt.sid 
        form.district.data = dt.dname
    dt=db1.query.all()
    return render_template('district.html', title='district',
                           form=form,dt=dt,state=state,legend='Update district')

@Admin.route("/dist/<int:did>/delete", methods=['GET', 'POST'])
@login_required
def delete_dist(did):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    dist = db1.query.get_or_404(did)
    db.session.delete(dist)
    db.session.commit()
    flash('district has been removed!', 'success')
    return redirect(url_for('Admin.dist'))

@Admin.route('/cityform',methods=['GET', 'POST'])
@login_required
def cityform():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    form=cityForm()
    form.state.choices =[(s.id, s.state_name) for s in state.query.all()]
    form.district.choices = [(d.did, d.dname) for d in db1.query.filter_by(sid=form.state.data).all()]
    if form.validate_on_submit():
        cit = db2(cname=form.city.data,did=form.district.data)
        db.session.add(cit)
        db.session.commit()
    dt=db2.query.all()
    return render_template('city.html',title="city",dt=dt,form=form,dist=db1,legend='Add city')


@Admin.route("/cityform/<int:cid>/<int:d>/update", methods=['GET', 'POST'])
@login_required
def update_city(cid,d):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    dt = db2.query.get_or_404(cid)
    st = db1.query.get(d)
    form = UcityForm()
    form.state.choices =[(s.id, s.state_name) for s in state.query.all()]
    form.district.choices = [(d.did, d.dname) for d in db1.query.filter_by(sid=form.state.data).all()]
    if form.validate_on_submit():
        dt.cname = form.city.data
        dt.did=form.district.data
        db.session.commit()
        flash('district name has been updated!', 'success')
        return redirect(url_for('Admin.cityform'))
    elif request.method == 'GET':
        form.state.data = st.sid
        form.district.choices = [(st.did,st.dname)]
        form.city.data = dt.cname  
    dt=db2.query.all()
    return render_template('city.html', title='city',
                           form=form,dt=dt,dist=db1,legend='Update city')

@Admin.route("/cityform/<int:cid>/delete", methods=['GET', 'POST'])
@login_required
def delete_city(cid):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    city = db2.query.get_or_404(cid)
    db.session.delete(city)
    db.session.commit()
    flash('city has been removed!', 'success')
    return redirect(url_for('Admin.cityform'))


@Admin.route('/cylinder',methods=['GET', 'POST'])
@login_required
def cylinder():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    form=cilyForm()
    form.state.choices =[(s.id, s.state_name) for s in state.query.all()]
    form.district.choices = [(d.did, d.dname) for d in db1.query.filter_by(sid=form.state.data).all()]
    form.agency_name.choices = [(a.aid, a.agency_name) for a in agent.query.filter_by(did=form.district.data).all()]
    st=None
    if form.validate_on_submit():
        if form.acylinder.data > 5:
            st='available'
        else:
            st='not available'
        c=cylinders.query.filter_by(aid=form.agency_name.data).first()
        if c:
            c.total_cylinder=form.tcylinder.data
            c.availabel_cylinder=form.acylinder.data
            c.status=st
        else:
            cyli=cylinders(aid=form.agency_name.data,total_cylinder=form.tcylinder.data,availabel_cylinder=form.acylinder.data,status=st)
            db.session.add(cyli)
        db.session.commit()
    cyli=cylinders.query.all()
    return render_template('cylinder.html',title="cylinder",cyli=cyli,agent=agent,dist=db1,form=form,legend='Add cylinder')

@Admin.route("/cylinder/<int:sno>/<int:aid>/update",methods=['GET', 'POST'])
@login_required
def update_cylinder(sno,aid):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    c = cylinders.query.get_or_404(sno)
    a = agent.query.get(aid)
    d = db1.query.get(a.did)
    form=UcilyForm()
    form.state.choices =[(s.id, s.state_name) for s in state.query.all()]
    form.district.choices = [(d.did, d.dname) for d in db1.query.filter_by(sid=form.state.data).all()]
    form.agency_name.choices = [(a.aid, a.agency_name) for a in agent.query.filter_by(did=form.district.data).all()]
    st=None
    if form.validate_on_submit():
        if form.acylinder.data > 5:
            st='available'
        else:
            st='not available'
        c.aid=form.agency_name.data
        c.total_cylinder=form.tcylinder.data
        c.availabel_cylinder=form.acylinder.data
        c.status=st
        db.session.commit()
        flash('cylinder details has been updated!', 'success')
        return redirect(url_for('Admin.cylinder'))
    elif request.method == 'GET':
        form.state.data = a.sid
        form.district.choices = [(d.did, d.dname)]
        form.agency_name.choices = [(a.aid,a.agency_name)]
        form.tcylinder.data = c.total_cylinder 
        form.acylinder.data = c.availabel_cylinder
    cyli=cylinders.query.all()
    return render_template('cylinder.html',title="cylinder",cyli=cyli,agent=agent,dist=db1,
                    form=form,legend='update cylinder')

@Admin.route("/cylinder/<int:sno>/delete", methods=['GET', 'POST'])
@login_required
def delete_cylinder(sno):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    cily = cylinders.query.get_or_404(sno)
    db.session.delete(cily)
    db.session.commit()
    flash('cylinder details has been removed!', 'success')
    return redirect(url_for('Admin.cylinder'))


@Admin.route('/connection',methods=['GET', 'POST'])
@login_required
def connection():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    form=ConForm()
    if form.validate_on_submit():
        c=connection_type.query.filter_by(ctid=form.connectionType.data).first()
        if c:
            c.refill_charge=form.rfillcharge.data
            c.new_connection_price=form.ncharge.data
        else:
            c=connection_type(cname=form.connectionType.data,
                refill_charge=form.rfillcharge.data,new_connection_price=form.ncharge.data)
            db.session.add(c)
        db.session.commit()
    cyli=connection_type.query.all()
    return render_template('connection.html',title="cylinder",cyli=cyli,form=form)


@Admin.route("/connection/<int:ctid>/delete", methods=['GET', 'POST'])
@login_required
def delete_connection(ctid):
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    ct = connection_type.query.get_or_404(ctid)
    db.session.delete(ct)
    db.session.commit()
    flash('connection details has been removed!', 'success')
    return redirect(url_for('Admin.connection'))

@Admin.route('/creport',methods=['GET', 'POST'])
@login_required
def creport():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    consumer=User_reg.query.all()
    return render_template('creport.html',title="consumerReport",consumer=consumer,ag=agent,dist=db1,state=state)

@Admin.route('/areport',methods=['GET', 'POST'])
@login_required
def areport():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    agents=agent.query.all()
    return render_template('areport.html',title="agentReport",agents=agents,dist=db1,state=state)

@Admin.route("/dregister", methods=['GET', 'POST'])
@login_required
def dregister():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    form = dRegistrationForm()
    form.state.choices =[(s.id, s.state_name) for s in state.query.all()]
    form.district.choices = [(d.did, d.dname) for d in db1.query.filter_by(sid=form.state.data).all()]
    form.city.choices = [(c.cid, c.cname) for c in db2.query.filter_by(did=form.district.data).all()]
    form.connectionType.choices = [(c.ctid,c.cname) for c in connection_type.query.all()]
    if form.validate_on_submit():
        hashed_pwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        cid=int(form.city.data)
        user = agent(fname=form.FirstName.data,lname=form.LastName.data,gender=form.Gender.data,phone_no=form.PhoneNo.data,adress=form.Address.data,sid=form.state.data,did=form.district.data,cid=cid,agency_name=form.agency_name.data,username=form.username.data,email=form.email.data,password=hashed_pwd)
        roleadd = roles(email=form.email.data,password=hashed_pwd,role='agent')
        db.session.add(user)
        db.session.add(roleadd)
        for choice in range(len(form.connectionType.data)):
            ct=db3.query.filter_by(ctid=form.connectionType.data[choice]).first()
            ct.agents.append(user)
            db.session.commit()
        db.session.commit()
        roleadd.aid=user.aid
        db.session.commit()
        flash(f'Your account has been created! now your able to login', 'success')
        return redirect(url_for('Admin.admin'))
    return render_template('dregister.html',title='register', form=form)

@Admin.route("/Alogin", methods=['GET', 'POST'])
def Alogin():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = roles.query.filter_by(email=form.email.data).first()
        if user and user.role=='admin' and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Main.home'))
        else:
            flash('Login Unsuccessfull. Please check email and password', 'danger')
    return render_template('Alogin.html', title='Login', form=form)

@Admin.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Main.home'))

@Admin.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    return render_template('admin.html',title='admin')

@Admin.route('/district/<st>')
def district(st):
    dist = db1.query.filter_by(sid=int(st)).all()

    distArray = []

    for d in dist:
        distObj = {}
        distObj['id'] =d.did
        distObj['name'] = d.dname
        distArray.append(distObj)

    return jsonify({'dist' : distArray})

@Admin.route('/city/<di>')
def city(di):
    cities = db2.query.filter_by(did=int(di)).all()

    cityArray = []

    for city in cities:
        cityObj = {}
        cityObj['id'] = city.cid
        cityObj['name'] = city.cname
        cityArray.append(cityObj)

    return jsonify({'cities' : cityArray})


@Admin.route('/agency_name/<di>')
def agency_name(di):
    agents = agent.query.filter_by(did=int(di)).all()

    ageArray = []

    for age in agents:
        ageObj = {}
        ageObj['id'] = age.aid
        ageObj['name'] = age.agency_name
        ageArray.append(ageObj)

    return jsonify({'agents' : ageArray})


@Admin.route('/connectionType/<age>')
def connectionType(age):
    cnid = connection_type.query.filter(connection_type.agents.any(aid=age)).all()

    conArray = []

    for connection in cnid:
        connectionOBJ = {}
        connectionOBJ['id'] = connection.ctid
        connectionOBJ['name'] = connection.cname
        conArray.append(connectionOBJ)

    return jsonify({'cnid' : conArray})

@Admin.route("/AfeedBack",methods=['GET','POST'])
def AfeedBack():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    afback = feedback.query.filter_by(aid=agent.aid).all()
    cfback = feedback.query.filter_by(uid=User_reg.id).all()
    ufback = feedback.query.filter_by(role='user').all()
    return render_template('ACfeedbackReport.html',afback=afback,cfback=cfback,ufback=ufback,title="feedback report",user=User_reg,agent=agent)


@Admin.route("/Cbox",methods=['GET','POST'])
def Cbox():
    if current_user.is_authenticated and current_user.role=='admin':
        pass
    else:
        abort(403)
    clist = feedback.query.filter_by(role='complaint').all()
    return render_template('Cbox.html',clist=clist,title="Consumer complaints",userR=User_reg,agent=agent)
