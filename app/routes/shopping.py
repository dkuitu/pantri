from flask import Blueprint, render_template, request, redirect, url_for
from app import db

bp = Blueprint('shopping', __name__, url_prefix='/shopping')

@bp.route('/')
def index():
    return render_template('shopping/index.html')
