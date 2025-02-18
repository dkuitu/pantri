from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from app.models.recipe import Recipe, Tag, RecipeIngredient, RecipeStep

bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@bp.route('/')
def index():
    try:
        current_app.logger.info('Accessing recipes index')
        # Get all tags for the filter dropdown
        tags = Tag.query.order_by(Tag.name).all()
        current_app.logger.debug(f'Found {len(tags)} tags')
        
        # Base query
        query = Recipe.query
        
        # Apply search if provided
        search = request.args.get('q')
        if search:
            current_app.logger.debug(f'Searching for: {search}')
            query = query.filter(Recipe.title.ilike(f'%{search}%'))
        
        # Apply tag filter if provided
        tag_id = request.args.get('tag')
        if tag_id:
            current_app.logger.debug(f'Filtering by tag_id: {tag_id}')
            query = query.filter(Recipe.tags.any(Tag.id == tag_id))
        
        # Apply quick filter if provided
        filter_type = request.args.get('filter')
        if filter_type == 'favorites':
            query = query.filter_by(is_favorite=True)
        elif filter_type == 'quick':
            query = query.filter(Recipe.total_time <= 30)
        elif filter_type == 'vegetarian':
            query = query.filter_by(is_vegetarian=True)
        
        # Get the filtered recipes
        recipes = query.order_by(Recipe.title).all()
        current_app.logger.debug(f'Found {len(recipes)} recipes')
        
        return render_template('recipes/index.html', recipes=recipes, tags=tags)
    except Exception as e:
        current_app.logger.error(f'Error in recipes index: {str(e)}')
        db.session.rollback()
        flash('An error occurred while loading recipes', 'error')
        return render_template('recipes/index.html', recipes=[], tags=[])

@bp.route('/add', methods=['GET', 'POST'])
def add():
    try:
        current_app.logger.info('Accessing recipe add page')
        tags = Tag.query.order_by(Tag.name).all()
        
        if request.method == 'POST':
            current_app.logger.debug('Processing POST request for new recipe')
            try:
                # Create new recipe
                recipe = Recipe(
                    title=request.form['title'],
                    description=request.form.get('description'),
                    prep_time=int(request.form['prep_time']) if request.form.get('prep_time') else None,
                    cook_time=int(request.form['cook_time']) if request.form.get('cook_time') else None,
                    servings=int(request.form['servings']) if request.form.get('servings') else None,
                    difficulty=request.form.get('difficulty'),
                    is_vegetarian=bool(request.form.get('is_vegetarian')),
                )

                # Add tags
                if request.form.getlist('tags'):
                    selected_tags = Tag.query.filter(Tag.id.in_(request.form.getlist('tags'))).all()
                    recipe.tags.extend(selected_tags)

                # Add ingredients
                quantities = request.form.getlist('ingredient_quantity[]')
                units = request.form.getlist('ingredient_unit[]')
                names = request.form.getlist('ingredient_name[]')
                
                for i in range(len(names)):
                    if names[i].strip():  # Only add if name is not empty
                        ingredient = RecipeIngredient(
                            name=names[i],
                            quantity=float(quantities[i]) if quantities[i] else None,
                            unit=units[i] if units[i] else None
                        )
                        recipe.ingredients.append(ingredient)

                # Add instructions
                instructions = request.form.getlist('instructions[]')
                for i, instruction in enumerate(instructions, 1):
                    if instruction.strip():  # Only add if instruction is not empty
                        step = RecipeStep(
                            step_number=i,
                            instruction=instruction
                        )
                        recipe.instructions.append(step)

                db.session.add(recipe)
                db.session.commit()
                
                flash('Recipe added successfully!', 'success')
                return redirect(url_for('recipes.index'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding recipe: {str(e)}', 'danger')
                return render_template('recipes/add.html', tags=tags), 400

        return render_template('recipes/add.html', tags=tags)
    except Exception as e:
        current_app.logger.error(f'Error in recipe add: {str(e)}')
        db.session.rollback()
        flash('An error occurred', 'error')
        return render_template('recipes/add.html', tags=[])

@bp.route('/generate')
def generate():
    return render_template('recipes/generate.html')

@bp.route('/<int:recipe_id>')
def view(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipes/view.html', recipe=recipe)
