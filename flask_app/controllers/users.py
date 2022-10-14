from flask_app import app 
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.hand_receipt import Hand_receipt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 


@app.route("/")
def index():
    session.clear()
    return render_template("registration.html")

@app.route("/users/register", methods=["POST"]) # route for register user. Route in registration.html
def register_user():
    if not User.validate_user(request.form):
        print("not valid")
        return redirect("/") #incorrect registration, dont need to change
    else:
        print("It is valid")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = { #modify data to match users table
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    user_id = User.save(data) # user_id is the variable for class method save in model
    print(f"Your user id is {str(user_id)}")
    session["user_id"] = user_id
    return redirect("/")

@app.route("/users_login", methods=["POST"]) # route for login. Route in registration .html
def login_user():
    print(request.form["email"])
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    
    if not user_in_db:
        flash("invalid email/password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid email/password")
        return redirect("/")
    
    session["user_id"] = user_in_db.id
    return redirect("/main")

@app.route("/main") # route for main page after login.
def main_page():
    print("is there user in in session: " + f"{session.get('user_id')}")
    if session.get("user_id") == None:
        return redirect("/")
    
    data = {
        "id": session["user_id"]
    }
    logged_user = User.get_by_id(data)
    hand_receipts = Hand_receipt.get_all(data)
    all_hand_receipts = Hand_receipt.all_hand_receipts_with_users()
    print(hand_receipts)
    return render_template("main.html", logged_user=logged_user, all_hand_receipts=all_hand_receipts)



