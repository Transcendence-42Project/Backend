# auth42/urls.py
from django.urls import path
from .views import auth, callback, login_view, register

urlpatterns = [
    path('', auth, name='auth'),  # Ana URL auth view'ine yönlendirilir
    path('callback/', callback, name='callback'),  # Geri dönüş URL'si
    path('login/', login_view, name='login'),  # Login view
    path('register/',register, name='register'),  # Register view
    
]