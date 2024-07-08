from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(response, *args, **kwargs):
	return HttpResponse("<h1>Here We Are!</h1>")