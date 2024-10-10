from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

#7.urls for crud
from rest_framework.routers import DefaultRouter

urlpatterns= [
    path('register/', RegisterView.as_view(), name= 'register'),
    path('login/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),

]

router= DefaultRouter()
router.register(r'items',Itemviewset)

urlpatterns+=router.urls