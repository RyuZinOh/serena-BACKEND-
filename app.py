from flask import Flask
from flask_marshmallow import Marshmallow
from config import Config
from db import mongo  # Import mongo from db.py
app = Flask(__name__)

app.config.from_object(Config)

mongo.init_app(app)
ma = Marshmallow(app)


##user
from routes.user_routes import user_bp
app.register_blueprint(user_bp)

#authentication
from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp)


##admin
from routes.admin_routes import admin_bp
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)