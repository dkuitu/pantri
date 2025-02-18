from flask import Blueprint, render_template
from app.models.pantry import PantryItem
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('home.html')
