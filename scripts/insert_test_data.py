from app import create_app, db
from app.models.recipe import Recipe, Tag, RecipeIngredient, RecipeStep
from app.models.location import Location
from app.models.pantry import PantryItem
from datetime import datetime, timedelta

def insert_test_data():
    app = create_app()
    with app.app_context():
        try:
            # Clear existing data - order matters for foreign key constraints
            RecipeIngredient.query.delete()
            RecipeStep.query.delete()
            
            # Delete all recipes (this will also clear the recipe_tags association table)
            Recipe.query.delete()
            
            # Delete remaining tables
            Tag.query.delete()
            PantryItem.query.delete()
            Location.query.delete()
            
            db.session.commit()
            
            print("Existing data cleared successfully!")
            
            # Create locations
            locations = [
                Location(name='Fridge'),
                Location(name='Freezer'),
                Location(name='Pantry'),
                Location(name='Spice Rack'),
                Location(name='Cupboard')
            ]
            for loc in locations:
                db.session.add(loc)
            db.session.commit()

            # Create tags
            tags = [
                Tag(name='Breakfast'),
                Tag(name='Lunch'),
                Tag(name='Dinner'),
                Tag(name='Dessert'),
                Tag(name='Snack'),
                Tag(name='Italian'),
                Tag(name='Asian'),
                Tag(name='Mexican')
            ]
            for tag in tags:
                db.session.add(tag)
            db.session.commit()

            # Create pantry items
            pantry_items = [
                ('Pasta', 500, 'g', 'Pantry', None),
                ('Rice', 1000, 'g', 'Pantry', None),
                ('Flour', 2000, 'g', 'Pantry', None),
                ('Sugar', 1000, 'g', 'Pantry', None),
                ('Salt', 500, 'g', 'Spice Rack', None),
                ('Pepper', 200, 'g', 'Spice Rack', None),
                ('Milk', 2000, 'mL', 'Fridge', datetime.now() + timedelta(days=7)),
                ('Eggs', 12, 'items', 'Fridge', datetime.now() + timedelta(days=14)),
                ('Butter', 500, 'g', 'Fridge', datetime.now() + timedelta(days=30)),
                ('Chicken Breast', 1000, 'g', 'Freezer', datetime.now() + timedelta(days=90)),
                ('Ground Beef', 500, 'g', 'Freezer', datetime.now() + timedelta(days=90)),
                ('Tomato Sauce', 500, 'mL', 'Pantry', datetime.now() + timedelta(days=180)),
                ('Olive Oil', 750, 'mL', 'Pantry', None),
                ('Garlic', 5, 'items', 'Pantry', None),
                ('Onions', 3, 'items', 'Pantry', None)
            ]

            for name, qty, unit, loc_name, expiry in pantry_items:
                location = next(l for l in locations if l.name == loc_name)
                item = PantryItem(
                    name=name,
                    quantity=qty,
                    unit=unit,
                    location_id=location.id,
                    expiry_date=expiry
                )
                db.session.add(item)
            db.session.commit()

            # Create recipes
            recipes_data = [
                {
                    'title': 'Classic Spaghetti Carbonara',
                    'description': 'A creamy Italian pasta dish with eggs, cheese, and pancetta',
                    'prep_time': 15,
                    'cook_time': 20,
                    'servings': 4,
                    'tags': ['Dinner', 'Italian'],
                    'ingredients': [
                        (400, 'g', 'Spaghetti'),
                        (200, 'g', 'Pancetta, diced'),
                        (4, 'items', 'Eggs'),
                        (100, 'g', 'Parmesan cheese, grated'),
                        (2, 'items', 'Garlic cloves'),
                        (2, 'tbsp', 'Olive oil'),
                        (1, 'tsp', 'Black pepper')
                    ],
                    'instructions': [
                        'Bring a large pot of salted water to boil',
                        'Cook spaghetti according to package instructions',
                        'Meanwhile, fry pancetta with garlic in olive oil',
                        'Beat eggs with grated cheese and pepper',
                        'Combine hot pasta with pancetta, then mix in egg mixture',
                        'Serve immediately with extra cheese and pepper'
                    ]
                },
                {
                    'title': 'Simple Chocolate Cake',
                    'description': 'Rich and moist chocolate cake perfect for any occasion',
                    'prep_time': 20,
                    'cook_time': 35,
                    'servings': 8,
                    'tags': ['Dessert'],
                    'ingredients': [
                        (250, 'g', 'All-purpose flour'),
                        (200, 'g', 'Sugar'),
                        (50, 'g', 'Cocoa powder'),
                        (2, 'items', 'Eggs'),
                        (250, 'mL', 'Milk'),
                        (100, 'g', 'Butter'),
                        (1, 'tsp', 'Vanilla extract')
                    ],
                    'instructions': [
                        'Preheat oven to 180°C',
                        'Mix dry ingredients in a bowl',
                        'Combine wet ingredients separately',
                        'Mix wet and dry ingredients until smooth',
                        'Pour into a greased cake pan',
                        'Bake for 35 minutes or until done'
                    ]
                }
            ]

            for recipe_data in recipes_data:
                recipe = Recipe(
                    title=recipe_data['title'],
                    description=recipe_data['description'],
                    prep_time=recipe_data['prep_time'],
                    cook_time=recipe_data['cook_time'],
                    servings=recipe_data['servings']
                )

                # Add tags
                recipe_tags = Tag.query.filter(Tag.name.in_(recipe_data['tags'])).all()
                recipe.tags.extend(recipe_tags)

                # Add ingredients
                for qty, unit, name in recipe_data['ingredients']:
                    ingredient = RecipeIngredient(
                        quantity=qty,
                        unit=unit,
                        name=name
                    )
                    recipe.ingredients.append(ingredient)

                # Add instructions
                for i, instruction in enumerate(recipe_data['instructions'], 1):
                    step = RecipeStep(
                        step_number=i,
                        instruction=instruction
                    )
                    recipe.instructions.append(step)

                db.session.add(recipe)
            
            db.session.commit()
            print("Test data inserted successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            raise

if __name__ == '__main__':
    insert_test_data() 