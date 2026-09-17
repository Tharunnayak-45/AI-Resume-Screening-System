from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config.db_config import get_db_connection


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()
            connection.close()

            return "Email already registered."

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (
                name,
                email,
                hashed_password
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            # Store user information in session
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            return redirect(
                url_for("auth.dashboard")
            )

        return "Invalid email or password."

    return render_template(
        "login.html"
    )


@auth_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            filename,
            skills,
            uploaded_at
        FROM resumes
        WHERE user_id = %s
        ORDER BY uploaded_at DESC
        """,
        (user_id,)
    )

    resumes = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        user_name=session["user_name"],
        resumes=resumes,
        resume_count=len(resumes)
    )


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )