from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField, EmailField

#6. CRUD views
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

#8.logging
import logging

#10 redis

from .utils import *




# Create your views here.

logger=logging.getLogger(__name__)

class Registerserializer(ModelSerializer):
    password= CharField(write_only=True)

    class Meta:
        model= User
        fields= [
            'username', 'email', 'password'
        ]

    def create(self, valdata):
        user= User.objects.create_user(
            username= valdata['username'],
            email= valdata['email'],
            password= valdata['password'],
        )

        return user
    
class RegisterView(generics.CreateAPIView):
    queryset= User.objects.all()
    permission_classes= [AllowAny]
    serializer_class= Registerserializer



class Itemviewset(viewsets.ModelViewSet):
    queryset= Items.objects.all()
    serializer_class= Itemserializer
    permission_classes= [IsAuthenticated]
    
    @cache_response(cache_key=lambda view, request, *args, **kwargs:f'item_{kwargs["pk"]}')
    def retrieve(self, request, *args, **kwargs):
        item_id= kwargs.get('pk')
        cached_item= cache.get(f'item_{item_id}')

        if cached_item:
            return Response(cached_item, status=status.HTTP_200_OK)
        
        try:
            item= self.get_object()
        except Items.DoesNotExist:
            logger.error(f'item {item_id} not found.')
            return Response({"error": "item not found"},status= status.HTTP_404_NOT_FOUND)
        
        serializer= self.get_serializer(item)
        cache.set(f'item_{item_id}',serializer.data,timeout=3600)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        data= request.data
        if Items.objects.filter(name=data.get('name')).exists():
            return Response({"error": "Item already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer= self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        item_id= kwargs.get('pk')

        try:
            item= self.get_object()
        except Items.DoesNotExist:
            return Response({"error":"item not found"},status=status.HTTP_404_NOT_FOUND)
        serializer= self.get_serializer(item,data=request.data, partial=False)    
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        cache.delete(f'item_{item_id}')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        item_id= kwargs.get('pk')
        try:
            item=self.get_object()
        except Items.DoesNotExist:
            return Response({"error":"item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(item)
        cache.delete(f'item_{item_id}')
        return Response({"message":"item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)