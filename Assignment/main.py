from flask import Flask, request, redirect, render_template
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

"""
username =
password =
verify_password =
email =
submit

"""

app = Flask(__name__)
app.config['DEBUG'] = True

name= ''
password= ''
password_verify = ''
email = ''

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/validata", methods=["POST"])
def validate_input():
    name = request.form['name']

    error= ''

    if not name:
        error += "You must enter a username.\n"
        name = ''
    else:
        if "" in name:
            error += "Your username connot contain a space.\n"
            name = ''

        elif len(name) < 3 or len(name) > 20:
            error +="Your username must be 3-20 characters.\n"

    password = request.form['password']
    password_verify = request.form['password_verify']

    pass_error = ''
    ver_error = ''

    if not password:
        pass_error += "You must enter a password.\n"
        password = ''
    else:
        if " " in password:
            pass_error += "Your password connot contain a space. \n"
            password = ''

        elif len(password) < 3 or len(password) > 20:
            pass_error +="Your password must be 3-20 characters.\n"
            password = ''

    if not password_verify: 
        ver_error += "You must verify your password.\n"
        password_verify = ''

    else:
        if password != password_verify:
            ver_error += "Your passwords do not match.\n"
            password_verify = ''

    email = request.form['email']

    e_error =''

    if email:
        if("@" not in email) or (' ' in email) or email.count('.') !=1:
            e_error += "Please enter a valid e-mail address.\n"
            email= ' '
        elif (len(email) < 3) or (len(email) > 20):
            e_error += "Your e-mail address should be between 3 and 20 characters.\n"
            email= ''

    if error == '' and pass_error == '' and ver_error == '' and e_error =='':
        return redirect('/valid-input?name={0}'.format(name))
    else:
        password = ''
        password_verify = ''
        return render_template('index.html', name=name, name_error=error, email=email, password=password, password_verify=password_verify, password_error=pass_error, pass_match_error=ver_error, email_error=e_error)
    
@app.route('/valid-input')
def valid_inpiut():
    name=request.args.get('name')
    return render_template('welcome.html', name=name)

app.run()