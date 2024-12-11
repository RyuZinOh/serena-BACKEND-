from db import mongo

def get_user_currency(user_id):
    currency = mongo.db.currency.find_one(
        {"user_id": user_id},
        {"coin_logo": 0}  # Exclude coin_logo field
    )
    
    if currency:
        return {
            "coin_name": currency.get("coin_name"),
            "coin_value": currency.get("serenex_balance")
        }
    
    return None

def get_user_photo(user_id):
    user_data = mongo.db.users.find_one(
        {"user_id": user_id},
        {"photo": 1, "_id": 0}  
    )
    
    if user_data and "photo" in user_data:
        return {
            "photo": user_data["photo"]
        }
    
    return None
