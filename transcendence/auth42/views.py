# auth42/views.py
import requests
from django.http import JsonResponse
from django.contrib.auth import authenticate
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
import random
import string


CLIENT_ID = 'u-s4t2ud-6c3e3891d90c9f5d7889d3a8a362bad7d2a33fc167b16958518f007df50b6cf6'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://localhost:8000/'  # Geri dönüş URL'si düzeltildi
AUTH_URL = 'https://api.intra.42.fr/oauth/authorize'
TOKEN_URL = 'https://api.intra.42.fr/oauth/token'
SCOPES = 'public'  # İzin vermek istediğiniz kapsamları belirtin

def generate_random_state(length=16):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

STATE = generate_random_state()

def auth(request):
    # OAuth 2.0 yetkilendirme URL'sini oluşturun
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
        'state': STATE,
        'response_type': 'code',
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"

    # Kullanıcıyı yetkilendirme ekranına yönlendirin
    return redirect(auth_url)

def callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    # Güvenlik kontrolü: 'state' değerlerini karşılaştırın
    if state != STATE:
        return JsonResponse({'error': 'Invalid state parameter'}, status=400)

    # Erişim belgesi için istek parametrelerini oluşturun
    token_params = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }

    try:
        # Erişim belgesini almak için isteği gönderin
        token_response = requests.post(TOKEN_URL, data=token_params)
        token_response.raise_for_status()
        access_token = token_response.json().get('access_token')

        # Erişim belgesi ile istenilen API isteğini gönderin (örneğin, '/v2/me' endpoint'i)
        api_response = requests.get('https://api.intra.42.fr/v2/me', headers={
            'Authorization': f'Bearer {access_token}',
        })
        api_response.raise_for_status()

        # API yanıtını istemciye gönderin
        return JsonResponse(api_response.json())
    except requests.exceptions.RequestException as e:
        print('OAuth Hatası:', e)
        return JsonResponse({'error': 'OAuth işlemi sırasında bir hata oluştu'}, status=500)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Kullanıcı kimlik bilgilerini doğrula
    user = authenticate(request, username=username, password=password)

    if user is None:
        # Kullanıcı kimlik bilgileri yanlış
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Kullanıcı kimlik bilgileri doğru, sadece JWT access token oluştur
    access_token = AccessToken.for_user(user)

    # Token içine username claim'ini ekleyin
    access_token['username'] = user.username

    return Response({
        'access': str(access_token),
    })




@csrf_exempt
@require_POST
def register(request):
    try:
        # İstek verilerini alalım
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Gerekli alanların olup olmadığını kontrol edelim
        if not email or not username or not password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # CustomUser modelini alalım
        User = get_user_model()

        try:
            # Yeni kullanıcıyı oluşturalım
            user = User.objects.create_user(email=email, username=username, password=password)

            # Başarılı yanıt döndürelim
            return JsonResponse({'success': 'User registered successfully'}, status=201)
        except Exception as e:
            # Hata durumunda uygun yanıtı döndürelim
            return JsonResponse({'error': str(e)}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)