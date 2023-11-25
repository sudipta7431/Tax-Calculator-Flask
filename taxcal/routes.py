from taxcal import *
from taxcal.models import *
from flask import Flask, make_response, redirect, render_template, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
import os
import pdfkit
import taxcal.tax as tax


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# REGETRATION FUNCTION
@app.route('/Signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['f_name'].capitalize()
        pan = request.form['pan'].upper()
        pic = request.files['pic']
        pic_name = pan+'.jpg'
        new_user = User(
            first_name=first_name,
            last_name=request.form['l_name'].capitalize(),
            email=request.form['email'],
            address=request.form['address'],
            postcode=request.form['postcode'],
            state=request.form['state'],
            birth_date=request.form['birth_date'],
            gender=request.form['gender'],
            mob=request.form['mob'],
            pan=request.form['pan'].upper(),
            pic=pic_name,
            password=request.form['password'],
        )
        if request.form['con_password'] == new_user.password:
            if User.query.filter_by(email=new_user.email).first() == None:
                if User.query.filter_by(pan=new_user.pan).first() == None:
                    db.session.add(new_user)
                    db.session.commit()
                    pic.save(os.path.join(app.root_path,
                             'static/images', pic_name))
                    logout_user()
                    flash('Successfully registered!', 'success')
                    return redirect(url_for('register'))
                else:
                    flash('PAN already registered', 'danger')
                    return redirect(url_for('register'))
            else:
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))
        else:
            flash('Password not match', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html')


# LOGIN FUNCTION
@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user)
                flash('Login successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong email & password', 'danger')
                return redirect(url_for('login'))
        else:
            flash('User not found', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


# USER DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():
    tax_data = Tax.query.filter_by(owner=current_user.id)
    return render_template('dashboard.html',tax_data=tax_data)

#DELETE TAX RECORDE
@app.route('/dashboard/delete/<int:id>')
@login_required
def delete(id):
    tax_data = Tax.query.filter_by(id=id).first()
    if current_user.id == tax_data.owner:
        db.session.delete(tax_data)
        db.session.commit()
        flash('Data delete successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('No data present', 'danger')
        return redirect(url_for('dashboard'))


# USER TAX CALCULATOR
@app.route('/TaxCalculator', methods=['GET', 'POST'])
@login_required
def calculator():
    if request.method == 'POST':
        gross_sal = request.form['gross_sal']
        basic_sal = request.form['basic_sal']
        helth_ins = request.form['helth_ins']
        insurance_premium = request.form['insurance_premium']
        house_ln_principle = request.form['house_ln_principle']
        house_ln_intarest = request.form['house_ln_intarest']
        Donation = request.form['Donation']
        nps = request.form['nps']
        # tax calculation
        old_tax, new_tax, pf, c80, d80, hra, deduction = tax.return_tax(int(gross_sal), int(basic_sal), int(
            helth_ins), int(insurance_premium), int(house_ln_principle), int(house_ln_intarest), int(Donation), int(nps))
        # database TAX
        new_tax_data = Tax(
            gross_sal=gross_sal,
            basic_sal=basic_sal,
            helth_ins=helth_ins,
            insurance_premium=insurance_premium,
            house_ln_principle=house_ln_principle,
            house_ln_intarest=house_ln_intarest,
            Donation=Donation,
            nps=nps,
            pf=pf,
            c80=c80,
            d80=d80,
            hra=hra,
            deduction=deduction,
            old_taxble_income=int(gross_sal)-int(deduction)-50000,
            old_tax=int(old_tax),
            new_tax=int(new_tax),
            new_taxble_income=int(gross_sal)-50000,
            owner=current_user.id
        )
        db.session.add(new_tax_data)
        db.session.commit()
        return render_template('calculator.html', gross_sal=gross_sal, basic_sal=basic_sal, insurance_premium=insurance_premium, house_ln_principle=house_ln_principle, house_ln_intarest=house_ln_intarest, helth_ins=helth_ins, Donation=Donation, nps=nps, old_tax=old_tax, new_tax=new_tax, pf=pf, c80=c80, d80=d80, hra=hra, old_taxble_income=(int(gross_sal)-int(deduction)-50000),new_taxble_income=(int(gross_sal)-50000),deduction=deduction)
    return render_template('calculator.html')

#previous data show
@app.route('/calculator/<int:id>')
@login_required
def calculate(id):
    userid = current_user.id
    tax = Tax.query.filter_by(id=id).first()
    if userid == tax.owner:
        gross_sal=tax.gross_sal
        basic_sal=tax.basic_sal
        helth_ins=tax.helth_ins
        insurance_premium=tax.insurance_premium
        house_ln_principle=tax.house_ln_principle
        house_ln_intarest=tax.house_ln_intarest
        Donation=tax.Donation
        nps=tax.nps
        pf=tax.pf
        c80=tax.c80
        d80=tax.d80
        hra=tax.hra
        deduction=tax.deduction
        old_taxble_income=tax.old_taxble_income
        old_tax=tax.old_tax
        new_tax=tax.new_tax
        new_taxble_income=tax.new_taxble_income
        return render_template('tax_edit.html', data_id = id, gross_sal=gross_sal, basic_sal=basic_sal, insurance_premium=insurance_premium, house_ln_principle=house_ln_principle, house_ln_intarest=house_ln_intarest, helth_ins=helth_ins, Donation=Donation, nps=nps, old_tax=old_tax, new_tax=new_tax, pf=pf, c80=c80, d80=d80, hra=hra, old_taxble_income=old_taxble_income,new_taxble_income=new_taxble_income,deduction=deduction)

#previous data edit
@app.route('/calculator/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_calculator(id):
    tax_data = Tax.query.filter_by(id=id).first()
    if request.method == 'POST':
        gross_sal = request.form['gross_sal']
        basic_sal = request.form['basic_sal']
        helth_ins = request.form['helth_ins']
        insurance_premium = request.form['insurance_premium']
        house_ln_principle = request.form['house_ln_principle']
        house_ln_intarest = request.form['house_ln_intarest']
        Donation = request.form['Donation']
        nps = request.form['nps']
        # tax calculation
        old_tax, new_tax, pf, c80, d80, hra, deduction = tax.return_tax(int(gross_sal), int(basic_sal), int(
            helth_ins), int(insurance_premium), int(house_ln_principle), int(house_ln_intarest), int(Donation), int(nps))
        tax_data.gross_sal=gross_sal
        tax_data.basic_sal=basic_sal
        tax_data.helth_ins=helth_ins
        tax_data.insurance_premium=insurance_premium
        tax_data.house_ln_principle=house_ln_principle
        tax_data.house_ln_intarest=house_ln_intarest
        tax_data.Donation=Donation
        tax_data.nps=nps
        tax_data.pf=pf
        tax_data.c80=c80
        tax_data.d80=d80
        tax_data.hra=hra
        tax_data.deduction=deduction
        tax_data.old_taxble_income=int(gross_sal)-int(deduction)-50000
        tax_data.old_tax=int(old_tax)
        tax_data.new_tax=int(new_tax)
        tax_data.new_taxble_income=int(gross_sal)-50000

        db.session.add(tax_data)
        db.session.commit()
        return render_template('tax_edit.html', gross_sal=gross_sal, basic_sal=basic_sal, insurance_premium=insurance_premium, house_ln_principle=house_ln_principle, house_ln_intarest=house_ln_intarest, helth_ins=helth_ins, Donation=Donation, nps=nps, old_tax=old_tax, new_tax=new_tax, pf=pf, c80=c80, d80=d80, hra=hra, old_taxble_income=tax_data.old_taxble_income,new_taxble_income=tax_data.new_taxble_income,deduction=deduction)


# USER PROFILE
@app.route('/Profile')
@login_required
def profile():
    return render_template('profile.html')


#PDF PRINT
@app.route('/statement/<int:id>')
@login_required
def pdf_print(id):
    tax_data = Tax.query.filter_by(id=id).first()
    render = render_template('pdf.html',tax_data=tax_data)
    pdf = pdfkit.from_string(render, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=statement.pdf'
    return response
    

# USER PROFILE EDIT
@app.route('/Profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    id = current_user.id
    if request.method == 'POST':
        first_name = request.form['f_name']
        last_name = request.form['l_name'].capitalize()
        email = request.form['email']
        address = request.form['address']
        postcode = request.form['postcode']
        state = request.form['state']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        mob = request.form['mob']
        pan = request.form['pan'].upper()
        #pic = request.files['pic']
        #print(pic)
        # picture
        #pic_name = pan+'.jpg'

        user = User.query.filter_by(id=id).first()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.address = address
        user.postcode = postcode
        user.state = state
        user.birth_date = birth_date
        user.gender = gender
        user.mob = mob
        user.pan = pan
        #user.pic = pic_name
        db.session.add(user)
        db.session.commit()
        #pic.save(os.path.join(app.root_path, 'static/images', pic_name))
        flash('Profile update Successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile_edit.html')

# USER PROFILE EDIT
@app.route('/Profile', methods=['GET', 'POST'])
@login_required
def picture_edit():
    id = current_user.id
    user = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        pan = user.pan
        pic = request.files['pic']
        pic_name = pan+'.jpg'
        user.pic = pic_name
        db.session.add(user)
        db.session.commit()
        pic.save(os.path.join(app.root_path, 'static/images', pic_name))
        flash('Profile update Successfully!', 'success')
        return redirect(url_for('profile'))

# USER PASSWORD CHANGE
@app.route('/Profile/Password', methods=['GET', 'POST'])
@login_required
def pass_change():
    id = current_user.id
    if request.method == 'POST':
        password = request.form['password']
        password_new = request.form['password_new']
        password_log = request.form['password_log']
        if password == current_user.password:
            if password_new == password_log:
                user = User.query.filter_by(id=id).first()
                user.password = password_log
                db.session.add(user)
                db.session.commit()
                flash('Password changed successfully!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('New password Not Match!', 'danger')
                return redirect(url_for('pass_change'))
        else:
            flash('Current Password Not Match!', 'danger')
            return redirect(url_for('pass_change'))
    return render_template('pass_change.html')


# LOGOUT USER
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))
