from flask import Flask, redirect, request, url_for, render_template, session, g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Email, EqualTo, Length
import email_validator
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SystemIntegration2'


class registerForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirmPassword = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Submit')

class loginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
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
    return get_loginForm()._csrf_token

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

@app.route("/regSubmit/" , methods=['GET', 'POST'])
def regSubmit():
    if get_regForm().validate_on_submit:
        return "This is a test that it has been submitted"

@app.route("/register/")
def register():
    if 'register' not in session:
        session['register'] = False
    session['register'] = True if session['register'] == False else False
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

    
if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app