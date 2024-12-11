from db import mongo
import base64

def get_user_currency(user_id):
    currency = mongo.db.currency.find_one({"user_id": user_id})

    if currency:
        coin_logo = currency.get("coin_logo")
    
        if isinstance(coin_logo, bytes):
            coin_logo = base64.b64encode(coin_logo).decode('utf-8')

        return {
            "coin_name": currency.get("coin_name"),
            "coin_value": currency.get("serenex_balance"),
            "coin_logo": coin_logo  
        }

    return None
