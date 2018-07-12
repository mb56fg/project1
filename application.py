import os
import requests, json
from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]      = "filesystem"

Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():

    # Get all of the users and passwords in the database, send them to our index.html template.
    rows = db.execute("SELECT * FROM users").fetchall()

    db.commit()

    return render_template("index.html", rows=rows)


@app.route("/", methods = ["POST"])
def login():

    # Get form information.

    username        =  request.form.get("username_f")
    password        =  request.form.get("password_f")

    if db.execute("SELECT COUNT(user_id) FROM users WHERE user_name = :username AND user_pw = :password ",
    {"username":username, "password":password}).scalar()==1:

        session['logged_in'] = username

        return render_template("indexl.html", user = session['logged_in'])

@app.route("/logout")
def logout():
    session.pop('logged_in',None)

    return render_template('bye.html')


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/search", methods = ["POST"])
def search():

    # Get form information.

    zipcode =  request.form.get("zip_f")

    #rows = db.execute("SELECT * FROM zipcodes WHERE zipcode = :zipcode",{"zipcode":zipcode}).fetchall()
    rows = db.execute("SELECT * FROM zipcodes WHERE zipcode = :zipcode",{"zipcode":zipcode}).fetchall()


    db.commit()

    return render_template('results.html',rows = rows)

#Info about City

@app.route("/info/<int:city_id>")
def info(city_id):
    latts =[]

    rows = db.execute("SELECT * FROM zipcodes WHERE id = :city_id",{"city_id":city_id}).fetchall()
    db.commit()

    latt = rows[0][4]
    long = rows[0][5]
    key     = "83984f460e3af01fb87fb1becd5a51a8/"
    string  = "https://api.darksky.net/forecast/" + key + str(latt) + "," + str(long)

    weather = requests.get(string).json()

    time    = weather["currently"]["time"]
    desc    = weather["currently"]["summary"]
    dew     = weather["currently"]["dewPoint"]
    temp    = weather["currently"]["temperature"]
    hum     = weather["currently"]["humidity"]

    return render_template('data.html',rows=rows, dew=dew, temp=temp, desc=desc,time=time, hum = hum)



@app.route("/api/<zipcode>")
def api(zipcode):

    row = db.execute("SELECT * FROM zipcodes WHERE zipcode =:zipcode", {"zipcode":zipcode})
    db.commit()

    latt = row[0][4]
    long = row[0][5]

    key     = "83984f460e3af01fb87fb1becd5a51a8/"
    string  = "https://api.darksky.net/forecast/" + key + str(latt) + "," + str(long)

    weather = requests.get(string).json()


    return render_template("hello")







@app.route("/register", methods=["POST"])
def register():

    # Get form information.

    user    =  request.form.get("username_f")
    passwd  =  request.form.get("password_f")

    if db.execute("Select user_name FROM users WHERE user_name = :username", {"username":user}).rowcount != 0:
         return render_template("regerror.html", message="That account name is already taken.")

    db.execute("INSERT INTO users (user_name, user_pw) VALUES (:username, :password)",
    {"username": user, "password": passwd})

    db.commit()

    return render_template("indexl.html")


