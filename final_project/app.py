from audioop import add
import os
import datetime
from pickle import APPEND

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, store_required
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///deliv.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

current_time = datetime.datetime.now()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
@store_required
def index():
    """assign driver to group of addresses with associated order number"""

    # Store a list of active drivers for the assoiciated store_id
    active_drivers = db.execute("SELECT name FROM drivers WHERE store_id = ? and active = ?", session["current_store_id"], "True")
    drivers = db.execute("SELECT name FROM drivers WHERE store_id = ?", session["current_store_id"])
    orders = db.execute("SELECT address, order_number FROM orders WHERE store_id = ?", session["current_store_id"])

    if not request.method == "POST":
        return render_template("index.html", active_drivers=active_drivers, drivers=drivers, orders=orders)

    if request.method == "POST":

        if request.form.get("activate") == "add":
            db.execute("UPDATE drivers SET active = ? WHERE name = ? AND store_id = ?", "True", request.form.get("driver"), session["current_store_id"])
            return redirect("/")

        elif request.form.get("activate") == "remove":
            db.execute("UPDATE drivers SET active = ? WHERE name = ? AND store_id = ?", "False", request.form.get("driver"), session["current_store_id"])
            return redirect("/")

        elif request.form.get("address_append") == "append":
            if not request.form.get("address"):
                return apology("Must enter an address", 400)

            elif not request.form.get("order_num"):
                return apology("Must enter an order number", 400)

            db.execute("INSERT INTO order (address, order_number, store_id) VALUES (?, ?, ?)", request.form.get("address"), request.form.get("order_num"), session["store_id"])
            return redirect("/")
    
    


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").upper())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/stores")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if not request.method == "POST":
        return render_template("register.html")

    #  Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400)

    # Ensure password was submit
    elif not request.form.get("password"):
        return apology("must provide password", 400)

    # Ensure confirmation password was submit
    elif not request.form.get("confirmation"):
        return apology("must confirm password", 400)

    # Ensure username doesnt already exist in DB
    if db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username").upper()):
        return apology("username already exists", 400)

    # Ensure password and confirmation password match
    if request.form.get("confirmation") == request.form.get("password"):

        # Insert new row into users table containing the filled forms data
        db.execute("INSERT INTO users (id, username, hash) VALUES (?, ?, ?)", id(request.form.get("username")), request.form.get(
            "username").upper(), generate_password_hash(request.form.get("password")))

    else:
        return apology("passwords do not match")

    # Redirect user to login page
    return redirect("/login")


@app.route("/stores", methods=["GET", "POST"])
@login_required
def stores():
    """change current store_id"""

    # Create a "stores" variable to hold any store_id associated to user
    stores = db.execute("SELECT DISTINCT st.store_id FROM stores st JOIN employees emp ON st.store_id = emp.store_id WHERE id = ?", session["user_id"])

    # Ensure "stores" variable is not empty
    if len(stores) <= 0:
        return redirect("/select_your_stores")

    # Load stores page
    if not request.method == "POST":
        return render_template("stores.html", stores=stores)

    # When form submit
    if request.method == "POST":

        # Set selected store_id as session variable
        if not request.form.get("current_store"):
            return apology("must select your store number", 400)
    
        # Set session[current_store_id] as selected store and redirect to homepage
        session["current_store_id"] = request.form.get("current_store")
        return redirect("/")


@app.route("/select_your_stores", methods=["GET", "POST"])
@login_required
def select_your_stores():
    """select the store/s to which the user is employed"""

    # Create a "stores" variable to hold all available store_id for the user to select from
    stores = db.execute("SELECT DISTINCT store_id FROM stores")
    if not request.method == "POST":
        return render_template("select_your_stores.html", stores=stores)

    if not request.form.get("store"):
        return apology("Please select a store number", 400)
    
    # Update users table with new store_id
    session["current_store_id"] = request.form.get("store")
    db.execute("INSERT INTO employees (id, store_id) VALUES (?, ?)", session["user_id"], session["current_store_id"])

    # If admin box checked prompt for passcode
    if request.form.get("admin") == "True":
        return redirect("/admin")

    return redirect("/stores")


@app.route("/admin", methods=["GET", "POST"])
@login_required
@store_required
def admin():
    """verify admin privileges via store password and updates user table with admin credentials"""

    # Store the store admin password to check agains users typed passcode
    password = db.execute("SELECT admin_passcode FROM stores WHERE store_id = ?", session["current_store_id"])

    # Render admin template    
    if not request.method == "POST":
        return render_template("admin.html")
    
    # When page submit
    if request.method == "POST":

        # If nothing entered return apology
        if not request.form.get("store_passcode"):
            return apology("Must enter password")

        # If passwords do not match return apology
        if request.form.get("store_passcode") != password[0]["admin_passcode"]:
            return apology("passwords do not match", 400)
    
        # If typed password matches store_password 
        if request.form.get("store_passcode") == password[0]["admin_passcode"]:
    
            # Update admin row on users table to give user admin priveleges and redirect to index
            db.execute("UPDATE employees SET admin = ? WHERE id = ? AND store_id = ?", "True", session["user_id"], session["current_store_id"])
            return redirect("/stores")

    

@app.route("/drivers", methods=["GET", "POST"])
@login_required
@store_required
def drivers():
    """add or remove employee from database"""

    # Store a list of all drivers for the assoiciated store_id
    drivers = db.execute("SELECT driver_id, name, store_id FROM drivers WHERE store_id = ?", session["current_store_id"])
    admin = db.execute("SELECT admin From employees WHERE store_id = ? AND id = ?", session["current_store_id"], session["user_id"])
    if not request.method == "POST":
        return render_template("drivers.html", drivers=drivers)

    # When page submit
    if request.method == "POST":

        # Emsure user has admin priveleges to append driver table
        if admin[0]["admin"] != "True":
            return apology("Admin Priveleges Required", 400)

        else:

            # If add driver button clicked
            if request.form["app_driver"] == "add":

                # Ensure driver name was submit
                if not request.form.get("name"):
                    return apology("Must submit name", 400)

                # Ensure driver name was submit
                if not request.form.get("id"):
                    return apology("Must submit id", 400)

                # Insert new row into drivers table with applicable data
                db.execute("INSERT INTO drivers (driver_id, name, store_id) VALUES (?, ?, ?)", request.form.get("id"), request.form.get ("name"), session.get("current_store_id"))
                return redirect("/drivers")

                # If remove driver button clicked
            if request.form["app_driver"] == "remove":

                # Ensure driver name was submit
                if not request.form.get("name"):
                    return apology("Must submit name", 400)

                # Ensure driver name was submit
                if not request.form.get("name"):
                    return apology("Must submit id", 400)
            
                # Remove any driver info from the drivers table matching submit form data
                db.execute("DELETE FROM drivers WHERE driver_id = ? AND name = ?", request.form.get("id"), request.form.get("name"))
                return redirect("drivers")



@app.route("/history", methods=["GET", "POST"])
@login_required
@store_required
def history():
    """shows table of dilivery history filterable by time passed"""
    return render_template("history.html")