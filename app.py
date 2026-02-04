from flask import Flask
from config import Config
from models import db
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp
from models import Admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()
    
    with app.app_context():
        db.create_all()
        
        if not Admin.query.filter_by(username="admin").first():
            admin = Admin(username="admin", password="admin123")
            db.session.add(admin)
            db.session.commit()


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
