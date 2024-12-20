from flask_marshmallow import Marshmallow
from bson import ObjectId

ma = Marshmallow()

class UserPFP_Schema(ma.Schema):
    class Meta:
        fields = ('user_id', 'pfp_file')
        
    user_id = ma.Str(dump_only=True)
    pfp_file = ma.Str(dump_only=True)  