from flask import Flask,url_for, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from cs50 import SQL
from validate_email import validate_email
from functools import wraps

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_NAME'] = 'your_cookie_name_here'
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///wishlist.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cach-Control"] = "no-cach, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    #forget any user_id
    session.clear()

    #User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        name = name.title()
        # Ensure username was submitted
        if not name:
            flash("Must provide username")

        # Ensure password was submitted
        elif not password:
            flash("Must provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", name)
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], password):
            flash("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session['logged_in'] = True

        # Redirect user to home page
        flash(f"Welcome {name}")
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

    session.clear()
    
    if request.method == "POST":

        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")
        valid_email = validate_email(email)
        rows = db.execute("SELECT * FROM users WHERE username = ?", name)
        email_check = db.execute("SELECT * FROM users WHERE email = ?", email)

        if not name or not password or not confirmation or not email:
            flash("Please fill out all required fields")
        elif rows:
            flash("Username already exists")
        elif password != confirmation:
            flash("Passwords not match")
        elif not valid_email:
            flash("Please provide a valid email address")
        elif email_check :
            flash("Sorry email Already exists")

        else:
            hashed_password = generate_password_hash(password)
            name = name.title()
            db.execute("INSERT INTO users (username, hash, email) VALUES(?, ?, ?)", name, hashed_password, email)
            
            user_id = db.execute("SELECT id FROM users WHERE username = ?", name)[0]["id"]
            
            session["user_id"] = user_id
            flash("Register Cmplete")
            return redirect("/")
    
    return render_template("/register.html")


@app.route("/", methods=["GET"])
@login_required
def index():
    
    rows = db.execute("SELECT * FROM wishes WHERE user_id = ?", session["user_id"])
    wishes = [{"name": row["wish"], "url": row["url"], "message": row["message"], "id": row["id"]} for row in rows]
    return render_template("index.html", wishes=wishes)


@app.route("/add", methods=["POST"])
@login_required
def add_wish():
    wish_name = request.form.get("wish")
    wish_url = request.form.get("url")
    wish_message = request.form.get("message") 



    if not wish_name:
        flash("Please insert your wish")
    else:
        if not wish_url:
            wish_url = "No URL"
        if not wish_message:
            wish_message = "No Message"
        
        wish_name = wish_name.title()
        db.execute("INSERT INTO wishes(user_id, wish, url, message) VALUES (?, ?, ?, ?)",
               session["user_id"], wish_name, wish_url, wish_message)
        db.execute(
            "INSERT INTO History (user_id, wish, url, message, timestamp)\
            VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
             wish_name,
             wish_url, 
             wish_message,
             datetime.now(),
        )
    
    return redirect(url_for('index'))


@app.route("/delete", methods=["POST"])
@login_required
def delete_wish():
    rows = db.execute("SELECT * FROM wishes where user_id = ?",
                      session["user_id"])
    wish_id = request.form["wish_id"]
    db.execute("DELETE FROM wishes WHERE id = ?\
            AND user_id = ?", wish_id, session["user_id"])
    
    return redirect(url_for('index'))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_name = ""
    old_password = None
    new_password = None
    conf_new_password = None
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        conf_new_password = request.form.get("conf_new_password")
        user_profile = db.execute(
            "SELECT username, hash\
                                  FROM users where id = ?",
            session["user_id"],
        )
        for row in user_profile:
            user_name = row["username"]
            user_password = row["hash"]

        unhashed_pass = check_password_hash(user_password, old_password)
        if not old_password:
            flash("MUST PROVIDE OLD PASSWORD")
        elif not unhashed_pass:
            flash("WRONG PASSWORD")
        elif not new_password or not conf_new_password:
            flash("MUST PROVIDE NEW PASSWORD")
        elif new_password != conf_new_password:
            flash("PASSWORDS DO NOT MATCH")

        hashed_password = generate_password_hash(new_password)

        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            hashed_password,
            session["user_id"],
        )

        flash("Password Changed Succssesfully!")
        return redirect("/")

    else:
        user_profile = db.execute(
            "SELECT username FROM users WHERE id = ?", session["user_id"]
        )
        for row in user_profile:
            user_name = row["username"]
        return render_template(
            "profile.html",
            user_name=user_name,
            old_password="",
            new_password="",
            conf_new_password="",
        )

@app.route("/history")
@login_required
def history():
    rows = db.execute(
        "SELECT wish, url, message, timestamp FROM HISTORY WHERE user_id = ?",
        session["user_id"],
    )
    wishes = []
    for row in rows:
        wish = row["wish"]
        url = row["url"]
        message = row["message"]
        time = row["timestamp"]
        wishes.append((wish, url, message, time))
    return render_template("history.html", wishes=wishes)


if __name__ == "__main__":
    app.run(debug=True)


