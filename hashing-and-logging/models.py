"""The overall goal of the code in "models.py" is to define and set up the data models for the Flask-feedback web application. These models are implemented using SQLAlchemy, a popular Object-Relational Mapping (ORM) tool for Flask, and they represent the structure of the underlying database. Here are the key components and goals of the code"""

"""Flask feedback models:"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create instances of Flask extensions
bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    # Connect the database to the Flask app
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    # Define columns for the 'users' table
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    # Define a relationship with the 'feedback' table
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    # Convenience class methods

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user, hashing their password."""
        # Hash the password using bcrypt and create a new user
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # Add the user to the database session
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        # Authenticate user by checking username and password
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    """Feedback."""

    __tablename__ = "feedback"

    # Define columns for the 'feedback' table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )
