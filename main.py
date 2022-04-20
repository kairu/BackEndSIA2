from flask import Flask, redirect, request, url_for, render_template, session, g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Email, EqualTo, Length
import pymongo as pm
import email_validator
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SystemIntegration2'

client = pm.MongoClient("mongodb+srv://test:test1234@demopy.8vbe5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
col = db["user"] 

app.config['MONGO_DBNAME'] = 'test'

class registerForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirmPassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Submit')

class loginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Submit')

def get_loginForm():
    if 'loginForm' not in g:
        g.loginForm = loginForm()
    return g.loginForm

def get_regForm():
    if 'regForm' not in g:
        g.regForm = registerForm()
    return g.regForm

@app.route("/login/", methods=['GET', 'POST'])
def get_user():
    if request.method == 'POST' and get_loginForm().validate_on_submit():
        username = get_loginForm().username.data
        password = get_loginForm().password.data
        qry = col.find_one({"username": username})
        if qry['password'] == password:
            session['username'] = username
            session.pop('register', None)
            return redirect(url_for('home'))
        else:
            return "Wrong password"

@app.route("/logout/")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/regSubmit/" , methods=['GET', 'POST'])
def regSubmit():
    if request.method == 'POST' and get_regForm().validate_on_submit():
        username = get_regForm().username.data
        password = get_regForm().password.data
        email = get_regForm().email.data
        qry = col.find_one({"username": username})
        if qry == None:
            col.insert_one({"username": username, "password": password, "email": email})
            session.pop('register', None)
            return redirect(url_for('home'))
        else:
            return "Username already exists"

def check_Session(content, data=None):
    if 'register' in session:
        if session['register']:
            if data == None:
                return render_template('index.html', mainContent=content+".html", form=get_regForm(), loginForm=get_loginForm())
            else:
                return render_template('index.html', mainContent=content+".html", form=get_regForm(), loginForm=get_loginForm(), data=data)
    else:
        if data == None:
            return render_template('index.html', mainContent=content+".html", loginForm=get_loginForm())
        else:
            return render_template('index.html', mainContent=content+".html", loginForm=get_loginForm(), data=data)

@app.route("/register/")
def register():
    if 'register' not in session:
        session['register'] = False
    session['register'] = True if session['register'] == False or 'register' not in session else session.pop('register', None)
    return redirect(url_for('home'))

@app.route("/")
def home():
    template = check_Session('home')
    return template

@app.route("/services/")
def services():
    template = check_Session('Services')
    return template

@app.route("/services/IDBM/")
def IDBM():
    template = check_Session('/Services/IDBM')
    return template

@app.route("/services/networksecurity/")
def netSec():
    template = check_Session('/Services/networkSecurity')
    return template

@app.route("/services/datastorage/")
def dataStorage():
    template = check_Session('/Services/dataStorage')
    return template

@app.route("/services/customersupport/")
def custSupp():
    template = check_Session('/Services/customerSupport')
    return template

@app.route("/services/networksetup/")
def netSetup():
    template = check_Session('/Services/networkSetup')
    return template

@app.route("/products/")
def products():
    data = json.load(open('productList.json'))
    template = check_Session('Products', data)
    return template

@app.route("/about/")
def about():
    template = check_Session('AboutCompany')
    return template

@app.route("/team/")
def team():
    template = check_Session('MeetTeam')
    return template

@app.route("/contact/")
def contact():
    template = check_Session('ContactUs')
    return template

@app.route("/test/", methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return "1"
    else:
        return "2"

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
