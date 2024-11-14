from flask import Flask
from flask_marshmallow import Marshmallow
from config import Config
from db import mongo  # Import mongo from db.py

app = Flask(__name__)
app.config.from_object(Config)

mongo.init_app(app)
ma = Marshmallow(app)

from routes.user_routes import user_bp
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
