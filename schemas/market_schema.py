from flask_marshmallow import Marshmallow

ma = Marshmallow()

class MarketSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'stats', 'image', 'price', 'content_type')

    stats = ma.fields.Dict(keys=ma.fields.String(), values=ma.fields.Integer())

    def dump(self, obj, many=False, **kwargs):
        result = super(MarketSchema, self).dump(obj, many=many, **kwargs)
        if many:
            for item in result:
                if item['image']:
                    item['image'] = str(item['image'])  # Convert binary to string
                    item['content_type'] = item['image'].content_type  # Add content_type
        else:
            if result['image']:
                result['image'] = str(result['image'])  # Convert binary to string
                result['content_type'] = result['image'].content_type  # Add content_type
        return result
