from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,ValidationError,InputRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6979@localhost/flask_login'
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = '12mkfloll'


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique = True,nullable=False)
    password = db.Column(db.String(30),nullable=False)

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Username'})
    password = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Password'})
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Username'})
    password = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Password'})
    submit = SubmitField('Register')
    def validate_user(self,username):
        existing_user = User.query.filter_by


@app.route('/')
def login():
    form = LoginForm()
    return render_template('login.html',form=form)

@app.route('/reg')
def register():
    form = RegisterForm()
    return render_template('register.html',form=form)

with app.app_context():

    db.create_all()
app.run(debug=True)