import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def store_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("current_store_id") is None:
            return redirect("/stores")
        return f(*args, **kwargs)
    return decorated_function

def api_call(orders):
    """
    This functions calls the google distance matrix api and returns results 
    """

    # Create partial url string variables to be combined for API request
    url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
    url2 = "&destinations="
    url3 = "&mode=car&key="
    api_key = "AIzaSyDNgpkzEyuqSt0eWFsMrqgSHzN8nBh2oyQ"
    origin = orders[0]["address"]
    destinations = ""
    for i in range(1, len(orders)):
        destinations += orders[i]["address"] + "|"
        full_url = url1+origin+url2+destinations+url3+api_key
        result = requests.get(full_url).json()
    return(result)