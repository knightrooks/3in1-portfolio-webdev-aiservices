from flask import Blueprint, render_template

# Create Blueprint
home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    """Homepage with 3-in-1 hero sections."""
    return render_template("home.html")


@home_bp.route("/about")
def about():
    """About page."""
    return render_template("about.html")
