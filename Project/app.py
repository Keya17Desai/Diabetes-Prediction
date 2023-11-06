
## Importing Packages


from datetime import datetime
from flask import Flask,render_template,url_for,flash,redirect,request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm,DataForm
from flask_bcrypt import Bcrypt
from flask_login import login_user,current_user,logout_user,login_required,LoginManager,UserMixin

import jsonify
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


## Initializing Packages


app=Flask(__name__)
model=pickle.load(open('Project\model.pkl','rb'))
app.config['SECRET_KEY']='30809af0a3532d59bc5aac47fce1cda4964944f236e766205b425c640fdbd10b'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'





## Models


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(20),nullable=False)
    lastname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120),nullable=False)
    password=db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}','{self.email}')"


class Data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    pregnancies=db.Column(db.String(20),nullable=False)
    glucose=db.Column(db.String(20),nullable=False)
    bloodpressure=db.Column(db.String(20),nullable=False)
    skinthickness=db.Column(db.String(20),nullable=False)
    insulin=db.Column(db.String(20),nullable=False)
    bmi=db.Column(db.String(20),nullable=False)
    diabetespedigreefunction=db.Column(db.String(20),nullable=False)
    age=db.Column(db.String(20),nullable=False)
    outcome=db.Column(db.String(20),nullable=False)
    #date_check=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"Data('{self.pregnancies}','{self.glucose}','{self.bloodpressure}','{self.skinthickness}','{self.insulin}','{self.bmi}','{self.diabetespedigreefunction}','{self.age}','{self.outcome}')"    
    




## Routes




@app.route('/')
@app.route('/home')
def home():
    image_file_1=url_for('static',filename='image/logo.JPG')
    image_file_2=url_for('static',filename='image/diabeteshead.jpg')
    image_file_3=url_for('static',filename='image/1.jpg')
    return render_template('home.html',image_file_1=image_file_1,image_file_2=image_file_2,image_file_3=image_file_3)


@app.route("/login", methods=['GET', 'POST'])
def login():
    image_file_5=url_for('static',filename='image/logo.JPG')
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (form.password.data==user.password):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form,image_file_5=image_file_5)


@app.route("/register", methods=['GET', 'POST'])
def register():
    image_file_4=url_for('static',filename='image/logo.JPG')
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.create_all()
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form,image_file_4=image_file_4)


@app.route('/test',methods=['POST','GET'])
def test():
    image_file_7=url_for('static',filename='image/logo.JPG')
    #image_file_8=url_for('static',filename='image/doctor.JPG')
    form=DataForm()
    if form.validate_on_submit():
        pregnancies=int(form.pregnancies.data)
        glucose=int(form.glucose.data)
        bloodpressure=int(form.bloodpressure.data)
        skinthickness=int(form.skinthickness.data)
        insulin=int(form.insulin.data)
        bmi=float(form.bmi.data)
        diabetespedigreefunction=float(form.skinthickness.data)
        age=int(form.age.data)
        prediction=model.predict([[pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi,diabetespedigreefunction,age]])
        output=prediction[0]
        if output==1:
            return redirect(url_for('success'))
        else:
            return redirect(url_for('fail'))
    return render_template('test.html',form=form,image_file_7=image_file_7)


@app.route('/success')
def success():
    image_file_6=url_for('static',filename='image/logo.JPG')
    return render_template('success.html',image_file_6=image_file_6)

@app.route('/fail')
def fail():
    image_file_6=url_for('static',filename='image/logo.JPG')
    return render_template('fail.html',image_file_6=image_file_6)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__=='__main__':
    app.run(debug=True)