# myapp/urls.py
from django.urls import path
from .views import get_data_from_api, post_data_to_api, auth, callback

urlpatterns = [
    path('get-data/', get_data_from_api, name='get_data'),
    path('post-data/', post_data_to_api, name='post_data'),
    path('', auth, name='auth'),  # Ana URL auth view'ine yönlendirilir
    path('callback/', callback, name='callback'),  # Geri dönüş URL'si
]