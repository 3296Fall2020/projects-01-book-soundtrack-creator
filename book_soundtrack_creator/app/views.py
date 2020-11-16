from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse, Http404
from .models import *
import spotipy
import spotipy.util as util
from spotipy import oauth2
# Create your views here.

scope = 'user-library-read'
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/callback/'
username = ''


def index(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')
    
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


def initial_sign_in(request):
    return render(request, 'initial_sign_in.html')

def sign_in(request):

    # token = util.prompt_for_user_token(username, scope)
    # print(token)
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, cache_path=".cache-" + username)
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return HttpResponseRedirect(auth_url)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    total = []
    results = sp.current_user_saved_tracks(limit=50)
    next = next_offset(results)

    total.append(results)
    while next and next < int(results['total']):
        next_50 = sp.current_user_saved_tracks(limit=50, offset=next)
        next = next_offset(next_50)
        total.append(next_50)
        print(next)
    tracks = []
    for r in total:
        for track in r['items']:
            tracks.append(track)

    return render(request, 'sign_in.html', {'results': tracks})
    