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

def book_emotion_classifier(request, *args, **kwargs):
    # book = Book.objects.create()

    # Extract the book text
    book = Book.objects.all().get(pk = kwargs["id"])
    bookText = book.bookText
    # print(bookText)
    bookText.open(mode='r')
    lines = bookText.readlines()
    bookText.close()
    
    # Call emotion classifier and analyze bookText (TO-DO: Figure out type of field (dictionary) and check correctness of algorithm)
    emotion = Book.emotion_classifier(lines)  # Returns a dictionary of {emotion: value}
    # emotion = "test emotion"
    book.bookEmotion = emotion
    book.save()
    return render(request, 'book_stats.html', {"book":book})
    