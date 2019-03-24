from projectmain import db,login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import CheckConstraint
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return roles.query.get(int(id))


class state(db.Model):
    """docstring for state"""
    id =db.Column(db.Integer,primary_key=True)
    state_name = db.Column(db.String(20),unique=True,nullable=False)
    district = db.relationship('district',cascade='all,delete',backref='state')

    def __repr__(self):
        return f"state('{self.id}', '{self.state_name}')"

class district(db.Model):
    did =db.Column(db.Integer,primary_key=True)
    dname = db.Column(db.String(20),nullable=False)
    sid = db.Column(db.Integer,db.ForeignKey('state.id'),nullable=False)
    city = db.relationship('city',cascade='all,delete',backref='district')
    agent = db.relationship('agent',cascade='all,delete',backref='district')
    user = db.relationship('User_reg',cascade='all,delete',backref='district')

    def __repr__(self):
        return f"district('{self.did}', '{self.dname}', '{self.sid}')"

class city(db.Model):
    cid =db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(20),nullable=False)
    did = db.Column(db.Integer,db.ForeignKey(district.did,ondelete="CASCADE"),nullable=False)

    def __repr__(self):
        return f"city('{self.cid}', '{self.cname}', '{self.did}')"

ctype = db.Table('ctype',
    db.Column('aid', db.Integer, db.ForeignKey('agent.aid',ondelete="CASCADE")),
    db.Column('ctid', db.Integer, db.ForeignKey('connection_type.ctid',ondelete="CASCADE"))
) 

class agent(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20),nullable=False)
    lname = db.Column(db.String(20),nullable=False)
    gender = db.Column(db.String(10),nullable=False)
    phone_no = db.Column(db.String(10),nullable=False)
    adress = db.Column(db.String(200),nullable=False)
    sid =db.Column(db.Integer,db.ForeignKey(state.id,ondelete="CASCADE"),nullable=False)
    did = db.Column(db.Integer,db.ForeignKey(district.did,ondelete="CASCADE"),nullable=False)
    cid = db.Column(db.Integer,db.ForeignKey(city.cid,ondelete="CASCADE"),nullable=False)
    agency_name = db.Column(db.String(40),unique=True,nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    ctype = db.relationship('connection_type', secondary=ctype,backref=db.backref('agents', lazy='dynamic'))
    cyli = db.relationship('cylinders',cascade='all,delete',backref='agent')
    book = db.relationship('booking',cascade='all,delete',backref='agent')
    rol = db.relationship('roles',cascade='all,delete',backref='agent')
    fbck = db.relationship('feedback',cascade='all,delete',backref='agent')
    def get_id(self):
           return (self.aid)

    def __repr__(self):
        return f"agent('{self.agency_name}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.aid}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return agent.query.get(user_id)


class connection_type(db.Model):
    """docstring for connection_type"""
    ctid = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(15),nullable=False)
    refill_charge = db.Column(db.Integer,nullable=False)
    new_connection_price = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"connection_type('{self.ctid}', '{self.cname}', '{self.refill_charge}'.'{self.new_connection_price}')"

class cylinders(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    aid = db.Column(db.Integer,db.ForeignKey(agent.aid,ondelete="CASCADE"),nullable=False)
    total_cylinder = db.Column(db.Integer,nullable=False)
    availabel_cylinder = db.Column(db.Integer,CheckConstraint('availabel_cylinder<=total_cylinder'),nullable=True)
    status = db.Column(db.String(10),nullable=False)

    def __repr__(self):
        return f"agent('{self.aid}','{self.total_cylinder}','{self.availabel_cylinder}','{self.status}')"


class User_reg(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20),nullable=False)
    lname = db.Column(db.String(20),nullable=False)
    gender = db.Column(db.String(10),nullable=False)
    phone_no = db.Column(db.String(10),nullable=False)
    adress = db.Column(db.String(200),nullable=False)
    sid =db.Column(db.Integer,db.ForeignKey(state.id,ondelete="CASCADE"),nullable=False)
    did = db.Column(db.Integer,db.ForeignKey(district.did,ondelete="CASCADE"),nullable=False)
    cid = db.Column(db.Integer,db.ForeignKey(city.cid,ondelete="CASCADE"),nullable=False)
    aid = db.Column(db.Integer,db.ForeignKey(agent.aid,ondelete="CASCADE"),nullable=False)
    ctid = db.Column(db.Integer,db.ForeignKey(connection_type.ctid,ondelete="CASCADE"),nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    fbck = db.relationship('feedback',cascade='all,delete',backref='User_reg')
    rol = db.relationship('roles',cascade='all,delete',backref='User_reg')
    def __repr__(self):
        return f"User_reg('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User_reg.query.get(user_id)

class roles(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(60),nullable=False)
    role = db.Column(db.String(10),nullable=False)
    uid = db.Column(db.Integer,db.ForeignKey(User_reg.id),nullable=True)
    aid = db.Column(db.Integer,db.ForeignKey(agent.aid),nullable=True)

    def __repr__(self):
        return f"roles('{self.email}', '{self.role}')"
        



class booking(db.Model):
    """docstring fss booking"""
    bid = db.Column(db.Integer,primary_key=True)
    bdate = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    ddate = db.Column(db.DateTime,nullable=True)
    uid = db.Column(db.Integer,db.ForeignKey(User_reg.id),nullable=False)
    aid = db.Column(db.Integer,db.ForeignKey(agent.aid),nullable=False)
    status = db.Column(db.String(20),nullable=False)
 
class feedback(db.Model):
    fid = db.Column(db.Integer,primary_key=True)
    sub = db.Column(db.String(20),nullable=False)
    description =db.Column(db.String(300),nullable=False)
    sdate = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    uid = db.Column(db.Integer,db.ForeignKey(User_reg.id),nullable=True)
    aid = db.Column(db.Integer,db.ForeignKey(agent.aid),nullable=True)
    role = db.Column(db.String(20),nullable=False)
