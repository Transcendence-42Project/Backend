import requests
from django.http import JsonResponse
from urllib.parse import urlencode
from django.shortcuts import redirect, render
import random
import string

def get_data_from_api(request):
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to retrieve data'}, status=response.status_code)
    
def post_data_to_api(request):
    url = 'https://jsonplaceholder.typicode.com/posts'
    payload = {
        'title': 'foo',
        'body': 'bar',
        'userId': 1
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to post data'}, status=response.status_code)



CLIENT_ID = 'u-s4t2ud-6c3e3891d90c9f5d7889d3a8a362bad7d2a33fc167b16958518f007df50b6cf6'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://localhost:8000'  # Geri dönüş URL'si düzeltildi
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