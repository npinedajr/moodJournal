from flask import Flask, request, jsonify, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import secrets

app = Flask(__name__)

secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(100),nullable=False)

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String,nullable=False)
    streak = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"{self.username} - {self.description}"

@app.route('/')
def index():
    return 'Welcome to Mood Journal! To get started, please use the guide.'

@app.route('/mood')
@login_required
# The get_moods function is called once the end point /mood is GET from. The function obtains
# all Mood record that have the same username saved as the current user logged in. All the 
# Mood records are printed, including their description, date, and streak values saved. 
def get_moods():
    mood_records = Mood.query.filter_by(username=current_user.username).all()
    output = []
    if not mood_records:
         return {"message": "No mood records currently stored!"}
    else: 
        for mood in mood_records:
            mood_data = {'description':mood.description, 'date':mood.date, 'streak':mood.streak}
            output.append(mood_data)
        return {"mood records": output}

@app.route('/mood',methods=['POST'])
@login_required
# The add_mood function is called once the end point /mood is POSTed to. The streak rating of the
# record is calculated by checking if at least one of the current mood records stored, for the currently 
# logged in user, was created the day before the one being currently created. The description of the record 
# is obtianed from user input and the username attribute of the record is set to the username of the 
# user that is currently logged in. 
def add_mood():
    today = datetime.date.today().strftime("%Y/%m/%d")
    previous_day = (datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y/%m/%d")
    mood_record = Mood.query.filter_by(username=current_user.username,date=previous_day).first()
    if not mood_record:
        streak = 1
    else:
        streak = mood_record.streak + 1
    mood = Mood(username=current_user.username, description=request.json['description'], date=today,streak=streak)
    db.session.add(mood)
    db.session.commit()
    return {'message':"Mood record successfuly added!"}

@app.route('/user',methods=['POST'])
# The create_user function will create a new user record if the /user end point if POSTed to. The password
# entered by the user is hashed to provide some security and the username attribute is set based on the 
# username entered by the user. 
def create_user():
    hash_pass = generate_password_hash(request.json['password'],method='sha256')
    user = User(username=request.json['username'],password=hash_pass)
    db.session.add(user)
    db.session.commit()
    return {"message": "Successfully created new user!"}

@app.route('/login', methods=['POST'])
# The login function will create a new user record if the /login end point if POSTed to. The
# function checks the inputs of the user to see if a username or password were entered and if the
# inputs match with the current records stored.
def login():
    authenticate = request.authorization 

    if not authenticate or not authenticate.username or not authenticate.password:
        return make_response("Unable to verify", 401)
    
    user = User.query.filter_by(username = authenticate.username).first()

    if not user:
        return make_response("User not found", 401)
    
    if check_password_hash(user.password,authenticate.password):
        login_user(user,remember=True)
        return {"message": "Successfully logged in!"}
    return make_response("Incorrect password for the username entered", 401)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return {"message": "Successfully logged out!"}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))