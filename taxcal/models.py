from taxcal import *
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(500), nullable=False)
    postcode = db.Column(db.String(6), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.String(12), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    mob = db.Column(db.String(10), nullable=False)
    pan = db.Column(db.String(10), nullable=False)
    pic = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tax = db.relationship('Tax', backref='owned_user', lazy=True)

class Tax(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gross_sal = db.Column(db.Integer, nullable=False)
    basic_sal = db.Column(db.Integer, nullable=False)
    helth_ins = db.Column(db.Integer, nullable=False)
    insurance_premium = db.Column(db.Integer, nullable=False)
    house_ln_principle = db.Column(db.Integer, nullable=False)
    house_ln_intarest = db.Column(db.Integer, nullable=False)
    Donation = db.Column(db.Integer, nullable=False)
    nps = db.Column(db.Integer, nullable=False)
    pf = db.Column(db.Integer, nullable=False)
    c80 = db.Column(db.Integer, nullable=False)
    d80 = db.Column(db.Integer, nullable=False)
    hra = db.Column(db.Integer, nullable=False)
    deduction = db.Column(db.Integer, nullable=False)
    old_taxble_income = db.Column(db.Integer, nullable=False)
    old_tax = db.Column(db.Integer, nullable=False)
    new_taxble_income = db.Column(db.Integer, nullable=False)
    new_tax = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))