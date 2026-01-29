from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.pantun_routes import pantun_bp
from routes.syair_routes import syair_bp
from models.user_model import db, bcrypt
import os

app = Flask(__name__)
CORS(app)

# Database config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(pantun_bp)
app.register_blueprint(syair_bp)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)






