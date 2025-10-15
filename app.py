from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages

# Hardcoded credentials for simulation
VALID_USERNAME = "user"
VALID_PASSWORD = "password"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return render_template("dashboard.html", username=username)
    else:
        flash("Invalid username or password!")
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
