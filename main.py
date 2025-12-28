from urllib.parse import quote

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user

from extensions import db
from models.user import User
from queries.user_queries import UserQueries

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CREATE DATABASE
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = quote("ashwath@MVN123")
DB_HOST = "localhost"

SQLALCHEMY_DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DB_URI
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)

user = User()
user_queries = UserQueries()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user_data = user_queries.get_user_by_id(user_id)["res"]

    return user_data

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["name"]
        password = generate_password_hash(request.form["password"], method="pbkdf2:sha256", salt_length=8)
        email = request.form["email"]

        user_by_email = user_queries.get_user_by_email(email)["res"]

        if len(user_by_email) != 0:
            flash("You have already signed up with that email, log in instead!")
            return redirect(url_for("login"))

        print(username, password, email)

        new_user = User(name=username, password=password, email=email)

        result = user_queries.add_user(new_user)

        login_user(new_user)

        return redirect(url_for("secrets"))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        result = user_queries.get_user_by_email(email)

        if len(result["res"]) == 0:
            flash("That email doesn't exist, Please try again!")
            return redirect(url_for("login"))

        if result["state"] == "success":
            user = result["res"][0]
            print(f"user logged ======> {user}")

            if check_password_hash(user.password, password):
                print("Password checking successful")
                login_user(user)

                return redirect(url_for("secrets"))
            else:
                print("Password checking failed")
                flash("Password incorrect, try again!")
                return redirect(url_for("login"))


    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    print("====================> calling secrets")
    print(current_user.name)
    # name = request.args.get("name")
    return render_template("secrets.html", name=current_user.name)


@app.route('/logout')
def logout():
    print("===================> calling logout")
    logout_user()

    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    print("====================> calling download")
    return send_from_directory("static", "files/cheat_sheet.pdf")


if __name__ == "__main__":
    with app.app_context():
        print("=========================> creating tables")
        db.create_all()
        print("=========================> finished creating tables")
    app.run(debug=True)
