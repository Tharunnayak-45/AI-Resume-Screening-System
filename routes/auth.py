from flask import Blueprint, render_template, request, redirect, session

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        session["user_email"] = email

        return redirect("/dashboard")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        return redirect("/login")

    return render_template("register.html")


@auth_bp.route("/dashboard")
def dashboard():

    if "user_email" not in session:
        return redirect("/login")

    user_name = session["user_email"].split("@")[0]

    return render_template(
        "dashboard.html",
        user_name=user_name,
        resumes=[]
    )


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")