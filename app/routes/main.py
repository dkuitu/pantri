from flask import Blueprint, render_template
from app.models.pantry import PantryItem
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    expiring_soon = PantryItem.query.filter(
        PantryItem.expiry_date <= datetime.now().date()
    ).limit(3).all()
    return render_template('home.html', expiring_soon=expiring_soon)
