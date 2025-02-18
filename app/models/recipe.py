from app import db
from datetime import datetime

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    servings = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))  # Easy, Medium, Hard
    is_favorite = db.Column(db.Boolean, default=False)
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_generated = db.Column(db.Boolean, default=False)  # True if LLM generated
    rating = db.Column(db.Float)  # 1-5 stars
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Recipe content
    ingredients = db.relationship('RecipeIngredient', backref='recipe', cascade='all, delete-orphan')
    instructions = db.relationship('RecipeStep', backref='recipe', order_by='RecipeStep.step_number', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary='recipe_tags', backref='recipes')

    @property
    def total_time(self):
        """Total time in minutes"""
        return (self.prep_time or 0) + (self.cook_time or 0)

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))
    note = db.Column(db.String(200))  # Optional notes like "finely chopped"

class RecipeStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# Association table for recipe tags
recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)
