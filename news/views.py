from django.shortcuts import render
import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello, World!")