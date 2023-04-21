from django.shortcuts import render
from .models import Category 
from .serializers import CategorySerializer


from rest_framework import generics, status
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.paginator import Paginator, EmptyPage




# Create your views here.

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset=MenuItem.objects.all()
#     serializer_class=MenuItemSerializer

# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset=MenuItem.objects.all()
#     serializer_class=MenuItemSerializer

from rest_framework.response import Response 
from rest_framework import viewsets 
from .models import MenuItem
from .serializers import MenuItemSerializer  

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class MenuItemsViewSet(viewsets.ModelViewSet):
    #throttle_classes=[AnonRateThrottle,UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price','inventory']
    search_fields=['title','category__title']


    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

# @api_view()
# def single_item(request, id):
#     item = get_object_or_404(Category,pk=id)
#     serialized_item = MenuItemSerializer(item)
#     return Response(serialized_item.data) 

# @api_view()
# def category_detail(request, pk):
#     category = get_object_or_404(Category,pk=pk)
#     serialized_category = CategorySerializer(category)
#     return Response(serialized_category.data) 