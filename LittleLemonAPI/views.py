from django.shortcuts import render
from .models import Category 
from .serializers import CategorySerializer


from rest_framework import generics, status
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response

from django.core.paginator import Paginator, EmptyPage

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle

from .throttles import TenCallsPerMinute

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
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

@api_view() #para verificar que el usuario tiene la key
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})


@api_view() #para verificar los permisos del usuario
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"only manager should see this"})
    else:
        return Response({"message": "You are not authorized"},403)
    
@api_view() #para limitar el llamado del endpoint de personas no autenticadas a 2 llamados por minuto
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})

@api_view() #para limitar el llamado del endpoint de personas autenticadas a 2 llamados por minuto
@permission_classes([IsAuthenticated])
#@throttle_classes([UserRateThrottle])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message":"message for the logged in users only"})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username=request.data['username']
    if username:
        user=get_object_or_404(User,username=username)
        managers=Group.objects.get(name="Manager")
        if request.method=='POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message":"ok"})
    return Response({'message':'error'},status.HTTP_400_BAD_REQUEST)