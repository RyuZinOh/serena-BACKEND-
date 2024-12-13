from db import mongo

def get_user_currency(user_id):
    currency = mongo.db.currency.find_one({"user_id": user_id})
    
    if currency:
        return {
            "coin_name": currency.get("coin_name"),
            "coin_value": currency.get("serenex_balance")
        }
    
    return None

