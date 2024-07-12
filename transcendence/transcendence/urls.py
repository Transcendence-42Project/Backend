# myproject/urls.py
from django.contrib import admin
from django.urls import path
from auth42.views import auth, callback , login_view , register


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', callback, name='callback'),  # Kök URL callback view'ine yönlendirir
    path('auth/', auth, name='auth'),  # auth42 URL yapılandırmasını dahil edin
    path('login/', login_view, name='login'),  # auth42 URL yapılandırmasını dahil edin
    path('register/',register, name='register'),  # Register view
]