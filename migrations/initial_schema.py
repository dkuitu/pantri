"""Initial schema

Revision ID: [will be auto-generated]
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

def upgrade():
    # Create location table
    op.create_table('location',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )

    # Create pantry_item table
    op.create_table('pantry_item',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['location.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create tag table
    op.create_table('tag',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create recipe table
    op.create_table('recipe',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('prep_time', sa.Integer(), nullable=True),
        sa.Column('cook_time', sa.Integer(), nullable=True),
        sa.Column('servings', sa.Integer(), nullable=True),
        sa.Column('difficulty', sa.String(length=20), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), default=False),
        sa.Column('is_vegetarian', sa.Boolean(), default=False),
        sa.Column('is_generated', sa.Boolean(), default=False),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )

    # Create recipe_ingredient table
    op.create_table('recipe_ingredient',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=20), nullable=True),
        sa.Column('note', sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create recipe_step table
    op.create_table('recipe_step',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('step_number', sa.Integer(), nullable=False),
        sa.Column('instruction', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create recipe_tags association table
    op.create_table('recipe_tags',
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id']),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id']),
        sa.PrimaryKeyConstraint('recipe_id', 'tag_id')
    )

    # Add default location
    op.execute("INSERT INTO location (name, description) VALUES ('Default', 'Default location')")

    # Add default tags
    op.execute("""
        INSERT INTO tag (name) VALUES 
        ('Quick Meals'),
        ('Vegetarian'),
        ('Breakfast'),
        ('Lunch'),
        ('Dinner'),
        ('Dessert'),
        ('Snack'),
        ('Healthy'),
        ('Comfort Food')
    """)

def downgrade():
    # Drop tables in reverse order
    op.drop_table('recipe_tags')
    op.drop_table('recipe_step')
    op.drop_table('recipe_ingredient')
    op.drop_table('recipe')
    op.drop_table('tag')
    op.drop_table('pantry_item')
    op.drop_table('location') 