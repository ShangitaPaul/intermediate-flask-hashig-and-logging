"""
- The purpose of this code to define and implement Flask forms for the Flask-feedback web application. These forms are used to handle user input for various functionalities within the application, including user authentication, registration, feedback submission, and account deletion. Each form corresponds to a specific type of user interaction

- These forms help ensure that user input is validated and meets certain criteria before being processed by the application. By using Flask-WTF and WTForms, the code simplifies the creation and validation of forms in the Flask framework, enhancing the security and reliability of the web application."""

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, Optional
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Login form."""
    
    # Username field with validation for required input and length constraints
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    
    # Password field with validation for required input and length constraints
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )


class RegisterForm(FlaskForm):
    """User registration form."""
    
    # Username field with validation for required input and length constraints
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    
    # Password field with validation for required input and length constraints
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    
    # Email field with validation for required input, email format, and length constraints
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    
    # First Name field with validation for required input and length constraints
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)],
    )
    
    # Last Name field with validation for required input and length constraints
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)],
    )


class FeedbackForm(FlaskForm):
    """Add feedback form."""
    
    # Title field with validation for required input and length constraints
    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    
    # Content field with validation for required input
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
    # This form is intentionally left blank as it is used for deletion confirmation.
