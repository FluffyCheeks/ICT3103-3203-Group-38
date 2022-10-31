from rest_framework import serializers 
from luna.models import *
 
 
class ProductSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product_Details
        fields = ('id',
                  'name',
                  'description',
                  'image',
                  'ingredients',
                  'unit_price',
                  'stock_available',
                  'category_id_id',
    )