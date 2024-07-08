# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from auth42.views import auth, callback, get_data_from_api, post_data_to_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', callback, name='callback'),  # Kök URL callback view'ine yönlendirir
    path('auth/', auth, name='auth'),  # auth42 URL yapılandırmasını dahil edin
    path('get-data/', get_data_from_api, name='get_data'),  # get-data URL yapılandırmasını dahil edin
    path('post-data/', post_data_to_api, name='post_data'),  # post-data URL yapılandırmasını dahil edin
]