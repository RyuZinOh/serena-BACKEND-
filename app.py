import os
from flask import Flask
from flask_marshmallow import Marshmallow
from config import Config
from db import mongo  



try:
    from extensions import socketio
except ImportError:
    import sys
    sys.path.append(os.path.dirname(__file__))
    from extensions import socketio

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return 'serena is running'

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


# pokempn spawner
from routes.pokemon_spawner import pokemon_spawner_bp
app.register_blueprint(pokemon_spawner_bp)


##currency
from routes.currency_users import currency_bp
app.register_blueprint(currency_bp)

## market
from routes.market_routes import market_bp
app.register_blueprint(market_bp)

#3 gettin my internet asset
from routes.global_fire import kamehameha_bp
app.register_blueprint(kamehameha_bp)


from extensions import socketio
from routes.chat_routes import chat_bp
app.register_blueprint(chat_bp)

# Initialize socketio
socketio.init_app(app)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run(debug=True)
    # socketio.run(app, host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=8080)
   