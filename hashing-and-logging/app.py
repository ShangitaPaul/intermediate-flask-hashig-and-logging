"""Feedback App:The overall purpose of this code is to implement a Flask web application for handling user registration, login, and feedback submission. The application allows users to register, log in, provide feedback, and manage their account. Here are the key functionalities and components"""

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

# Configure the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Enable the Debug Toolbar extension
toolbar = DebugToolbarExtension(app)

# Connect the app to the database
connect_db(app)


@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""
    return redirect("/register")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""
    # Check if the user is already logged in
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        # If form is submitted and validated, register the user
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        # If form is not validated, re-render the registration form
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""
    # Check if the user is already logged in
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        # If form is submitted and validated, log in the user
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            # If authentication fails, render the login form with an error message
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """Logout route."""
    # Logout the user by removing the 'username' from the session
    session.pop("username")
    return redirect("/login")


@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""
    # Check if the user is logged in and matches the requested user
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login."""
    # Check if the user is logged in and matches the requested user
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""
    # Check if the user is logged in and matches the requested user
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        # If form is submitted and validated, add new feedback
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        # If form is not validated, re-render the feedback form
        return render_template("feedback/new.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""
    # Retrieve the feedback with the given ID
    feedback = Feedback.query.get(feedback_id)

    # Check if the user is logged in and matches the feedback's owner
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        # If form is submitted and validated, update feedback
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""
    # Retrieve the feedback with the given ID
    feedback = Feedback.query.get(feedback_id)

    # Check if the user is logged in and matches the feedback's owner
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        # If form is submitted and validated, delete feedback
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
