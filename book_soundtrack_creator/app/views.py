from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404

# Create your views here.


def index(request):
    return render(request, 'home.html')

def book_selector(request):
    return render(request, 'book_selector.html')