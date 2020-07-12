#import files
from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash
from flask_session import Session
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

bot = ChatBot("AIO-BOT")
trainer = ListTrainer(bot)
trainer.train(['what is your name?', 'My name is AIO-BOT'])
trainer.train(['who are you?', 'I am a BOT'])
trainer.train(['my profile', 'Name: Kelvinkumar Mukeshkumar Patel, Class: CE-6-C, Attendance: 85%, CGPA: 8.69'])
trainer.train(['recent notice', 'Dear students of sem 4th,6th and 8th to enhance your employability and for your better performance in future placement drives, the Training and Placement cell has uploaded aptitude quiz in which you can appear voluntarily ( any time of your convenience -24/7 upto mid night of 3rd May) using your login credentials. This quiz will surely help you sharpen your aptitude ability to crack written test of various competitive exams as well.'])
trainer.train(['module solutions', 'https://drive.google.com/drive/folders/1X6JPZeOogFf0UxXpR5Rr23kEeA-xoFnW'])
trainer.train(['book appointment', "Sure, who's appointment: 1) HOD 2) Principal 3) CC"])
trainer.train(['3', "CC's appointment booked.  CC will contact you soon about the same"])
trainer.train(['time-table', "TIMETABLE - 6th CE - B 27-4-2020 Monday 10am to 10:50 am -TOC 10:50am to 11.30am - LIBRARY 12:00pm to 12.50pm - WT 12:50pm to 1.40pm - SE 2:00pm to 3.40pm - B1: AJ B2: AJ B3: WT"])
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("userhome"))
    else:
        return render_template("index.html")

@app.route("/userhome")
def userhome():
    if "user" in session:
        return render_template("userhome.html")
    else:
        return redirect(url_for("index"))


@app.route("/features")
def features():
    if "user" in session:
        return render_template("features.html");
    else: 
        return redirect(url_for("login"))

@app.route("/chatroom")
def chatroom():    
    if "user" in session:
        return render_template("chatroom.html");
    else: 
        return redirect(url_for("login"))

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')    
    return str(bot.get_response(userText)) 

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if "user" in session:
        return redirect(url_for("userhome"))
    else:
        if request.method == "POST":
            name = request.form["name"]
            # email = request.form["email"]
            # password = request.form["password"]
            # db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
            # {"username": name, "email": email, "password": password})
            # db.commit()
            session["user"] = name
            return redirect(url_for("userhome"))
        else:
            return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    # If user is already logged in
    if "user" in session:
        return redirect(url_for("userhome"))
    else:
        # If user submits credentials for logging in
        if request.method == "POST":
            name = request.form["name"]
            password = request.form["password"]
            # theuser = db.execute("SELECT * FROM users WHERE username = :username", {"username": name}).fetchone()
            # if theuser != None:
            #     if theuser.password == password:
            session["user"] = name
            return redirect(url_for("userhome"))
                # else:
                #     flash('Invalid username or password')
                #     return redirect(url_for("login"))      
            # else: 
            #     flash("The account doesn't exist.")
            #     return redirect(url_for("login"))
        else:
            return render_template("login.html")

@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("userhome"))

if __name__ == "__main__":    
    app.run()
