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

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes





# class MenuItemsView(generics.ListCreateAPIView):
#     queryset=MenuItem.objects.all()
#     serializer_class=MenuItemSerializer

# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset=MenuItem.objects.all()
#     serializer_class=MenuItemSerializer

@api_view(['GET','POST'])
def menu_items(request):
    if request.method=='GET':
        items = MenuItem.objects.select_related('category').all()
        category_name=request.query_params.get('category')
        to_price=request.query_params.get('to_price')
        search=request.query_params.get('search')
        ordering=request.query_params.get('ordering')
        perpage=request.query_params.get('pepage',default=2)
        page=request.query_params.get('page',default=1)

        if category_name:
            items=items.filter(category__title=category_name)
        if to_price:
            items=items.filter(price__lte=to_price)
        if search:
            items=items.filter(title__startswith=search)
        if ordering:
            #items=items.order_by(ordering) para ordenar por un campo
            ordering_fields=ordering.split(",")
            items=items.order_by(*ordering_fields)
        paginator=Paginator(items, per_page=perpage)
        try:
            items=paginator.page(number=page)
        except EmptyPage:
            items=[]


        serialized_item = MenuItemSerializer(items,many=True)
        return Response(serialized_item.data) 
    if request.method=='POST':
        serialized_item=MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED) 


@api_view()
def single_item(request, id):
    item = get_object_or_404(Category,pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data) 

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data) 

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})