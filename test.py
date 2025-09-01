from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecret"

# fake db
users = {
    "emad": generate_password_hash("1234")
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        print('post')
        username = request.form["username"]
        password = request.form["password"]

        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials"
    print('get')
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"Welcome {session['user']} to Dashboard"
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
