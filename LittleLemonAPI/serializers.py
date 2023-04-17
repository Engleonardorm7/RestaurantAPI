from rest_framework import serializers
from .models import MenuItem,Category
from decimal import Decimal
import bleach

from rest_framework.validators import UniqueValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer): # para crear hipervinculos  serializers.HyperlinkedModelSerializer
    # stock= serializers.IntegerField(source="inventory")#to change the name 
    price_after_tax=serializers.SerializerMethodField(method_name="calculate_tax")# to add a new field
    category=CategorySerializer(read_only=True)
    category_id=serializers.IntegerField(write_only=True)
    #depth=1
#------------para validar la informacion y que no se haga html injection

    def validate_title(self, value):
        return bleach.clean(value)
    # def validate(self, attrs):
    #     attrs['title'] = bleach.clean(attrs['title'])
    #     if(attrs['price']<2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')
    #     if(attrs['inventory']<0):
    #         raise serializers.ValidationError('Stock cannot be negative')
    #     return super().validate(attrs)
#--------------otra forma de validar datos:-----------------
#     def validate(self, attrs):
#         if(attrs['price']<2):
#             raise serializers.ValidationError('Price should not be less than 2.0')
#         if(attrs['inventory']<0):
#             raise serializers.ValidationError('Stock cannot be negative')
#         return super().validate(attrs)
    class Meta:
        model=MenuItem
        fields=['id','title','price',"stock","price_after_tax","category","category_id"]
        extra_kwargs = {
            'price': {'min_value': 2},
            'stock':{'source':'inventory', 'min_value': 0},
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all()
                    )
                ]
            }
            }
        



    def calculate_tax(self,product:MenuItem):
        return product.price*Decimal(1.1)
#------------Si solo se quiere mostrar el id y el title:------------
# class MenuItemSerializer(serializers.Serializer):

#     id=serializers.IntegerField()
#     title=serializers.CharField(max_length=255)
#     price=serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory=serializers.IntegerField()