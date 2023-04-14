from django.shortcuts import render

from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
# Create your views here.

class MenuItemsView(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer