from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from .models import *
# Create your views here.


def index(request):
    return render(request, 'home.html')

def book_selector(request):
    books = Book.objects.all()
    return render(request, 'book_selector.html', {'books' : books})

def set_user_info(request):
    response = ""
    email = ""
    name = ""
    userID = ""
    # if request.method == 'POST':
        # email = request.POST.get('email')
        # name = request.POST.get('name')
        # userID = request.POST.get('userID')
    
    user = User.objects.create()
    user.email = email
    user.name = name
    user.userID = userID
    user.save()
    return render(request, 'book_selector.html')
    