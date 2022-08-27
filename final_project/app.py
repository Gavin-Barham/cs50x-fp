import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")

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
        print(rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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

      # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 400)

    elif not request.form.get("confirmation"):
        return apology("must confirm password", 400)

    if db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username").upper()):
        return apology("username already exists", 400)

    if request.form.get("confirmation") == request.form.get("password"):
        # Query database for username
        db.execute("INSERT INTO users (id, username, hash) VALUES (?, ?, ?)", id(request.form.get("username")), request.form.get(
            "username").upper(), generate_password_hash(request.form.get("password")))
    else:
        return apology("passwords do not match")

    # Redirect user to login page
    return redirect("/login")

@app.route("/employee", methods=["GET", "POST"])
def employee():
    """add or remove employee from database"""

                '''TODO'''

    if not request.method == "POST":
        return render_template("employee.html")
    else:
    return redirect("assign.html")


@app.route("/history", methods=["GET", "POST"])
def history():
    """shows table of dilivery history filterable by time passed"""

                        '''TODO'''
                        
    return render_template("history.html")