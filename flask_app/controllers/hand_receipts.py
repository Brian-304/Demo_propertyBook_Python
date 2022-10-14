from flask_app import app
from flask import render_template, redirect, session, request # to implement and use routes
from flask_app.models.hand_receipt import Hand_receipt # impport models to work with tables in the database 
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

@app.route("/add/receipt")
def add_hand_receipt():
    print("valid")
    return render_template("create_hand_receipt.html")

@app.route("/hand_receipt/submit", methods=["POST"]) # route to submit inputs in the database 
def submit_cars():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "section": request.form["section"],
        "hand_receipt_number": request.form["hand_receipt_number"],
        "users_id": session["user_id"],
    }
    if not Hand_receipt.validation(data):
        return redirect("/add/receipt")
    Hand_receipt.save(data)
    return redirect("/main")


@app.route("/edit/<int:id>")
def edit_hand_receipt_page(id):
    one_hand_receipt = Hand_receipt.get_single_hand_receipt({"id":id})
    return render_template("edit_hand_receipt.html", one_hand_receipt=one_hand_receipt)

@app.route("/edit/<int:id>", methods=["POST"])
def submit_edit(id):
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "section": request.form["section"],
        "hand_receipt_number": request.form["hand_receipt_number"],
        "id":id
    }
    Hand_receipt.edit_hand_receipt(data)
    hand_receipts = Hand_receipt.get_all(data)
    return redirect("/main")

@app.route('/delete/<int:id>') # route to delete tree
def delete(id):
    data = {
        "id": id
    }
    Hand_receipt.delete(data)
    return redirect('/main')


@app.route("/end_items")
def end_items_page():
    return render_template("add_end_items.html")



