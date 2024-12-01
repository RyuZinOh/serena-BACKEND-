from werkzeug.security import check_password_hash, generate_password_hash
from db import mongo
import datetime
from config import Config
import jwt
from bson import ObjectId


def register_user(data):
    name = data['name']
    email = data['email']
    password = data['password']
    phone = data['phone']
    address = data['address']
    securityQues = data['securityQues']
    role = 0

    if len(name) < 3 or len(password) < 6:
        return {'message': 'Name must be at least 3 characters and password at least 6 characters.'}, 400

    user_collection = mongo.db.users
    existing_user = user_collection.find_one({'$or': [{'email': email}, {'phone': phone}]})
    if existing_user:
        return {'message': 'Email or phone already exists.'}, 400

    hashed_password = generate_password_hash(password)
    new_user = {
        'name': name,
        'email': email,
        'password': hashed_password,
        'phone': phone,
        'address': address,
        'securityQues': securityQues,
        'role': role
    }

    user_collection.insert_one(new_user)
    return {'message': 'User registered successfully'}, 201


def login_user(data):
    email = data['email']
    password = data['password']

    user_collection = mongo.db.users
    user = user_collection.find_one({'email': email})

    if user and check_password_hash(user['password'], password):
        user_data = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'phone': user['phone'],
            'address': user['address'],
            'securityQues': user['securityQues'],
            'role': user['role']
        }

        payload = {
            'sub': str(user['_id']),
            'name': user['name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
        
        return {'message': 'Login successful', 'user': user_data, 'token': token}, 200
    else:
        return {'message': 'Invalid email or password'}, 401

def handle_forgot_password(data):
    email = data['email']
    securityQues = data['securityQues']
    new_password = data['newPassword']

    user_collection = mongo.db.users
    user = user_collection.find_one({'email': email})

    if not user:
        return {'message': 'User with this email does not exist.'}, 404

    if user['securityQues'] != securityQues:
        return {'message': 'Incorrect security question answer.'}, 400

    hashed_password = generate_password_hash(new_password)
    user_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
    return {'message': 'Password updated successfully.'}, 200





def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

#user twekws
def update_user(user_id, data, token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id or logged_in_user_id != user_id:
        return {'message': 'Unauthorized!'}, 403

    update_data = {}
    if "name" in data:
        update_data["name"] = data["name"]
    if "email" in data:
        update_data["email"] = data["email"]
    if "phone" in data:
        update_data["phone"] = data["phone"]
    if "address" in data:
        update_data["address"] = data["address"]
    if "securityQues" in data:
        update_data["securityQues"] = data["securityQues"]

    result = mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return {'message': 'User not found or unauthorized!'}, 404

    return {'message': 'User updated successfully!'}, 200

def change_password(user_id, data, token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id or logged_in_user_id != user_id:
        return {'message': 'Unauthorized!'}, 403

    old_password = data['oldPassword']
    new_password = data['newPassword']

    user_collection = mongo.db.users
    user = user_collection.find_one({'_id': ObjectId(user_id)})

    if not user:
        return {'message': 'User not found!'}, 404

    if not check_password_hash(user['password'], old_password):
        return {'message': 'Old password is incorrect!'}, 400

    hashed_new_password = generate_password_hash(new_password)
    user_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'password': hashed_new_password}}
    )

    return {'message': 'Password changed successfully!'}, 200

def delete_user(user_id, token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id or logged_in_user_id != user_id:
        return {'message': 'Unauthorized!'}, 403

    user_collection = mongo.db.users
    result = user_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return {'message': 'User not found or unauthorized!'}, 404

    mongo.db.pokemons.delete_many({"user_id": ObjectId(user_id)})

    return {'message': 'User account deleted successfully!'}, 200



#adding pokemons
def add_pokemon(user_id, data, token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id:
        return {'message': 'Invalid or expired token!'}, 401

    if logged_in_user_id != user_id:
        return {'message': 'Unauthorized!'}, 403

    name = data.get('name')
    types = data.get('types', [])
    sprite = data.get('sprite')
    iv = data.get('iv', {})

    if not name or not sprite:
        return {'message': 'Name and sprite are required!'}, 400

    pokemon = {
        "user_id": ObjectId(user_id),
        "name": name,
        "types": types,
        "sprite": sprite,
        "iv": {
            "hp": iv.get('hp', 0),
            "attack": iv.get('attack', 0),
            "defense": iv.get('defense', 0),
            "special_attack": iv.get('special_attack', 0),
            "special_defense": iv.get('special_defense', 0),
            "speed": iv.get('speed', 0)
        }
    }

    mongo.db.pokemons.insert_one(pokemon)
    return {'message': 'Pokemon added successfully!'}, 201


#Getting users pokemon
def list_pokemons(user_id, token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id or logged_in_user_id != user_id:
        return {'message': 'Unauthorized!'}, 403

    pokemons = list(mongo.db.pokemons.find({"user_id": ObjectId(user_id)}))
    for pokemon in pokemons:
        pokemon["_id"] = str(pokemon["_id"])
        pokemon["user_id"] = str(pokemon["user_id"])

    return {'message': 'Pokemons retrieved successfully!', 'pokemons': pokemons}, 200

#Updatin it
def update_pokemon(user_id, pokemon_id, data, token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id or logged_in_user_id != user_id:
        return {'message': 'Unauthorized!'}, 403

    update_data = {}
    if "name" in data:
        update_data["name"] = data["name"]
    if "types" in data:
        update_data["types"] = data["types"]
    if "sprite" in data:
        update_data["sprite"] = data["sprite"]
    if "iv" in data:
        update_data["iv"] = {
            "hp": data["iv"].get("hp", 0),
            "attack": data["iv"].get("attack", 0),
            "defense": data["iv"].get("defense", 0),
            "special_attack": data["iv"].get("special_attack", 0),
            "special_defense": data["iv"].get("special_defense", 0),
            "speed": data["iv"].get("speed", 0),
        }

    result = mongo.db.pokemons.update_one(
        {"_id": ObjectId(pokemon_id), "user_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return {'message': 'Pokemon not found or unauthorized!'}, 404

    return {'message': 'Pokemon updated successfully!'}, 200

#deleitng pokemons
def delete_pokemon(user_id, pokemon_id, token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id or logged_in_user_id != user_id:
        return {'message': 'Unauthorized!'}, 403

    result = mongo.db.pokemons.delete_one({"_id": ObjectId(pokemon_id), "user_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return {'message': 'Pokemon not found or unauthorized!'}, 404

    return {'message': 'Pokemon deleted successfully!'}, 200
