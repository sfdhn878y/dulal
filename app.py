from flask import Flask, render_template,request,redirect,url_for
from extension import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False






db.init_app(app)
from models import *


@app.route('/')
def index():
    print('index funiton is cliced')
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login',methods=['GET','POST'])
def login():


    if request.method == 'POST':
        f_name = request.form.get('email')
        p_psw = request.form.get('password')

        print('fname:',f_name,'p_psw:',p_psw)
        ext_user= User.query.filter_by(email=f_name,password=p_psw).first()




        if ext_user and ext_user.role == "patient":

            return redirect(url_for('patient_dashbaord'))
        if ext_user and ext_user.role == "admin":

            return redirect(url_for('admin_dashbaord'))
            
        if ext_user and ext_user.role == "docotor":

            return redirect(url_for('doctor_dashbaord'))


    return render_template('login.html')


@app.route('/patient_dashbaord')
def patient_dashbaord():
    return render_template('patient_dashbaord.html')

@app.route('/admin_dashbaord')
def admin_dashbaord():
    return render_template('admin_dashbaord.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        f_name = request.form.get('username')
        p_psw = request.form.get('password')
        e_mail = request.form.get('email')
        gen_der = request.form.get('gender')
        ph=request.form.get('phone')
        aa=request.form.get('aadhar')
        address=request.form.get('address')
        dob_str = request.form.get('dob')
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()






        # Check if user already exists
        existing_user = User.query.filter_by(email=e_mail).first()
        if existing_user:
            return render_template('registration.html', message='User already registered! Please login.')


        # Create new user
        new_user = User(name=f_name,email=e_mail, password=p_psw , gender=gen_der,phone=ph,aadhar=aa,address=address,
                        dob=dob, role='patient')
        db.session.add(new_user)
        db.session.commit()


        return render_template('registration.html', message='Registration successful! You can now login.')


    return render_template('registration.html')






if __name__ == '__main__':
    with app.app_context():


        db.create_all()    
        existing_admin = User.query.filter_by(name="admin").first()
       
        if not existing_admin:
            admin_db = User(
                name="admin",
                password="admin",
                email="ds@gmail.com",
                role="admin",
            )
            db.session.add(admin_db)
            db.session.commit()
    app.run(debug=True)
