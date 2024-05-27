from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,ValidationError,InputRequired
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6979@localhost/flask_login'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = '12mkfloll'


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique = True,nullable=False)
    password = db.Column(db.String,nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True,nullable=False)
    buying = db.Column(db.Integer,nullable=False)
    selling = db.Column(db.Integer,nullable=False)
    stock = db.Column(db.Integer,nullable=False)

class ProductForm(FlaskForm):
    name = StringField(validators=[InputRequired()],render_kw={'placeholder':'Name'})
    buying = StringField(validators=[InputRequired()],render_kw={'placeholder':'Buying'})
    selling = StringField(validators=[InputRequired()],render_kw={'placeholder':'Selling'})
    stock = StringField(validators=[InputRequired()],render_kw={'placeholder':'Stock'})
    submit = SubmitField("Add New")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Username'})
    password = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Password'})
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Username'})
    password = StringField(validators=[InputRequired(),Length(min=4,max=100)],render_kw={'placeholder':'Password'})
    submit = SubmitField('Register')
    def validate_user(self,username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Username already exists. Please choose a different one")

@app.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html',form=form)

@app.route('/reg',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/product')
def product():
    form = ProductForm()
    # 
    return render_template('products.html',form=form)

@app.route('/add_p',methods=['GET','POST'])
def add_p():
    form = ProductForm
    new_product = Product(name = form.name.data, buying=form.buying.data, selling = form.selling.data, stock = form.selling.data)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('product'))


with app.app_context():
    db.create_all()
app.run(debug=True)