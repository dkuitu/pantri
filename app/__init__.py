from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'pantri.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import main, pantry, recipes, shopping, locations
    app.register_blueprint(main.bp)
    app.register_blueprint(pantry.bp)
    app.register_blueprint(recipes.bp)
    app.register_blueprint(shopping.bp)
    app.register_blueprint(locations.bp)

    # Make sure the main blueprint handles the root URL
    app.add_url_rule('/', endpoint='index')

    # Add error handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.error(f'403 error: {error}')
        return 'Forbidden Error: You don\'t have permission to access this resource', 403

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f'404 error: {error}')
        return 'Page Not Found', 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'500 error: {error}')
        db.session.rollback()
        return 'Internal Server Error', 500

    return app
