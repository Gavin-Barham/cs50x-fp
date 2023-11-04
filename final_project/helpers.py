from dotenv import dotenv_values
import requests

from flask import redirect, render_template, session
from functools import wraps

ENVIRON = dotenv_values(".env")


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
    api_key = ENVIRON["API_KEY"]
    origin = orders[0]["address"]
    destinations = ""
    MAX_TIME = 300

    # Dynamicaly set destinations
    for i in range(1, len(orders)):
        destinations += orders[i]["address"] + "|"

    if destinations == "":
        return

    # Concatinate full URl and call API
    full_url = url1+origin+url2+destinations+url3+api_key
    result = requests.get(full_url).json()

    # Format results for relevant information
    to_return = []

    try:
        result = result['rows'][0]['elements']
    except:
        return

    for i in range(1, len(orders)):
        api_data = result[i-1]
        time_in_seconds = api_data['duration']['value']

        # Ensure only duration less than 5 minutes returned
        if time_in_seconds <= MAX_TIME:
            to_return.append({
                'from': origin,
                'to': orders[i]['address'],
                'time_seconds': api_data['duration']['value'],
                'distance_meters': api_data['distance']['value'],
                'time_display_string': api_data['duration']['text'],
                'distance_display_string': api_data['distance']['text'],
            })

    # Return a list of formatted data
    return to_return
