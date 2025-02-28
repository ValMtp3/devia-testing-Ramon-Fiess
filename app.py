from flask import Flask
from models.database import db
from routes.user_routes import user_routes
from routes.service_routes import service_routes
from routes.commande_routes import commande_routes
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    migrate = Migrate(app, db)
    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Creates database tables if they don't exist

    # Register blueprints
    app.register_blueprint(user_routes, url_prefix="/api")
    app.register_blueprint(service_routes, url_prefix="/apii")
    app.register_blueprint(commande_routes, url_prefix="/apiii")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)
