from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from datetime import datetime
from app.models.pantry import PantryItem, Location

bp = Blueprint('pantry', __name__, url_prefix='/pantry')

@bp.route('/')
def index():
    # Get location filter from query parameters
    location_id = request.args.get('location_id', type=int)
    
    # Base query
    query = PantryItem.query
    
    # Apply location filter if specified
    if location_id:
        query = query.filter_by(location_id=location_id)
    
    # Get all locations for the filter buttons
    locations = Location.query.order_by(Location.name).all()
    selected_location = Location.query.get(location_id) if location_id else None
    
    # Get items with filters applied
    items = query.order_by(PantryItem.expiry_date.asc()).all()
    
    return render_template('pantry/index.html', 
                         items=items, 
                         locations=locations, 
                         selected_location=selected_location)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    locations = Location.query.order_by(Location.name).all()
    if request.method == 'POST':
        try:
            # Handle expiry date
            expiry_date = None
            if not request.form.get('no_expiry') and request.form.get('expiry_date'):
                expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()

            item = PantryItem(
                name=request.form['name'],
                quantity=float(request.form['quantity']),
                unit=request.form['unit'],
                location_id=int(request.form['location_id']),
                expiry_date=expiry_date
            )
            
            db.session.add(item)
            db.session.commit()
            flash('Item added successfully!', 'success')
            return redirect(url_for('pantry.index'))
        except ValueError as e:
            flash('Invalid input. Please check your values.', 'danger')
            return render_template('pantry/add.html', locations=locations), 400
        except Exception as e:
            flash(f'An error occurred while adding the item: {str(e)}', 'danger')
            return render_template('pantry/add.html', locations=locations), 500
    
    return render_template('pantry/add.html', locations=locations)

@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = PantryItem.query.get_or_404(item_id)
    locations = Location.query.order_by(Location.name).all()
    
    if request.method == 'POST':
        try:
            item.name = request.form['name']
            item.quantity = float(request.form['quantity'])
            item.unit = request.form['unit']
            item.location_id = int(request.form['location_id'])
            
            # Handle expiry date
            if request.form.get('no_expiry'):
                item.expiry_date = None
            elif request.form.get('expiry_date'):
                item.expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()
            
            db.session.commit()
            flash('Item updated successfully!', 'success')
            return redirect(url_for('pantry.index'))
        except ValueError:
            flash('Invalid input. Please check your values.', 'danger')
            return render_template('pantry/edit.html', item=item, locations=locations), 400
        except Exception as e:
            flash(f'An error occurred while updating the item: {str(e)}', 'danger')
            return render_template('pantry/edit.html', item=item, locations=locations), 500
    
    return render_template('pantry/edit.html', item=item, locations=locations)

@bp.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    item = PantryItem.query.get_or_404(item_id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred while deleting the item: {str(e)}', 'danger')
    return redirect(url_for('pantry.index'))
