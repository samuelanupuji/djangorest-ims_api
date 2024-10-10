from django.test import TestCase

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

#9. unit tests
from rest_framework import status



# Create your tests here.

class Itemtests(APITestCase):
    def setUp(self):
        self.user= User.objects.create_user(username='testuser',password='testpassword')
        self.token= RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION= f'Bearer {self.token}')
        self.item_data= {'name':'Test item','description':'A sample item', 'quantity':10}
        self.item= Items.objects.create(name='test item', description='sample description',quantity=10)

    def test_create_item(self):
        data={'name':'new item','description':'new item description','quantity':15}
        response= self.client.post('/items/',data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_item(self):
        item= Items.objects.create(name='Test item', description='A sample item', quantity= 10)
        response= self.client.get(f'/items/{item.id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_item(self):
        data={'name':'updated item', 'description':'updated description','quantity':20}
        response=self.client.put(f'/items/{self.item.id}/',data, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'],'updated item')

    def test_delete_item(self):
        response= self.client.delete(f'/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
    def test_get_item_from_cache(self):
        response=self.client.get(f'/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertNumQueries(0):
            response= self.client.get(f'/items/{self.item.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_authentication(self):
        self.client.credentials()
        response=self.client.get(f'/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
