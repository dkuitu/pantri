from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.pantry import Location

bp = Blueprint('locations', __name__, url_prefix='/locations')

@bp.route('/')
def index():
    locations = Location.query.order_by(Location.name).all()
    return render_template('locations/index.html', locations=locations)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            location = Location(
                name=request.form['name'],
                description=request.form.get('description', '')
            )
            db.session.add(location)
            db.session.commit()
            flash('Location added successfully!', 'success')
            return redirect(url_for('locations.index'))
        except Exception as e:
            flash(f'An error occurred while adding the location: {str(e)}', 'danger')
            return render_template('locations/add.html'), 500
    
    return render_template('locations/add.html')

@bp.route('/edit/<int:location_id>', methods=['GET', 'POST'])
def edit(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'POST':
        try:
            location.name = request.form['name']
            location.description = request.form.get('description', '')
            db.session.commit()
            flash('Location updated successfully!', 'success')
            return redirect(url_for('locations.index'))
        except Exception as e:
            flash(f'An error occurred while updating the location: {str(e)}', 'danger')
            return render_template('locations/edit.html', location=location), 500
    
    return render_template('locations/edit.html', location=location) 