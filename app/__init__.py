from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import main, pantry, recipes, shopping
    app.register_blueprint(main.bp)
    app.register_blueprint(pantry.bp)
    app.register_blueprint(recipes.bp)
    app.register_blueprint(shopping.bp)

    return app
