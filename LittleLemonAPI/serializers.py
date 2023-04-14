from rest_framework import serializers
from .models import MenuItem,Category
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock= serializers.IntegerField(source="inventory")#to change the name 
    price_after_tax=serializers.SerializerMethodField(method_name="calculate_tax")# to add a new field
    category=CategorySerializer()
    #depth=1
    class Meta:
        model=MenuItem
        fields=['id','title','price','inventory',"stock","price_after_tax","category"]
      
    def calculate_tax(self,product:MenuItem):
        return product.price*Decimal(1.1)
#------------Si solo se quiere mostrar el id y el title:------------
# class MenuItemSerializer(serializers.Serializer):

#     id=serializers.IntegerField()
#     title=serializers.CharField(max_length=255)
#     price=serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory=serializers.IntegerField()