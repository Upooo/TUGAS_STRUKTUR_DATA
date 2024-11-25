from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/pmb'
    app.config['SECRET_KEY'] = 'arya'
    
    db.init_app(app)
    
    from routes.adm import adm_bp
    from routes.auth import auth_bp
    from routes.mhs import mhs_bp
    from routes.index import index_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(adm_bp)
    app.register_blueprint(mhs_bp)
    app.register_blueprint(index_bp)

    return app