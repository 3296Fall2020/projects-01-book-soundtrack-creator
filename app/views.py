from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import *
from PIL import Image
from io import BytesIO
import spotipy
import spotipy.util as util
from spotipy import oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.util import prompt_for_user_token
from zipfile import ZipFile
from bs4 import BeautifulSoup
from tqdm import tqdm
from heapq import nlargest
import json
import re
import os
# generate random integer values
from random import seed
from random import randint
# seed random number generator
seed(1)


# Create your views here.

scope = 'user-library-read user-top-read user-follow-read'
SPOTIPY_CLIENT_ID = '1d19391e82ac405fb02f35ebf74cc767'
SPOTIPY_CLIENT_SECRET = '156400e3d8834a8395aaf95d420bb215'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/book_selector/'
username = ''
CACHE = '.spotipyoauthcache'

def index(request):
    # user = request.session['user']
    try:
        user = request.session['user']
    except:
        request.session['user'] = randint(0, 100)
        user = request.session['user']
    return render(request, 'home.html',{'user':user})

def test(request):
    count = 1
    requests_response = requests.get("http://127.0.0.1:8000/find_books/")
    try:
        user = request.session['user']
    except:
        request.session['user'] = randint(0, 100)
    # print(requests_response.content)
    # r = requests.get("http://gutendex.com/books/"+str(count)).json()
    # authors = set()
    # print('id' in r)
    # while(count < 67000):
        
    #     if(len(r['authors']) > 0):
    #         # for a in r['authors']  :
    #         print(r['authors'][0]['name'] + " " +str(count))    
    #         authors.add(r['authors'][0]['name'])
    #     count +=1
    #     r = requests.get("http://gutendex.com/books/"+str(count)).json()
    #     if(count % 100 == 0):
    #         print(str(count/65000) + "%")
    #     while(not('authors' in r)):
    #         print("missing response! " + str(count))
    #         count += 1
    #         r = requests.get("http://gutendex.com/books/"+str(count)).json()

    # print(authors)
    # while(requests.get("https://www.gutenberg.org/books/"+count)
    # requests_response = requests.get("https://www.gutenberg.org/browse/authors/a")
    # print(requests_response)
    soup = BeautifulSoup(requests_response, 'html.parser')
    # bookshelf = soup.find_all('li')
    # print("hellooooo" ,bookshelf)
    print(soup)
    django_response = HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )
    print(django_response.content)
    return django_response
    
    
def login(request):
    return render(request, 'login.html')

# call this after 1 hour of session time?
def refresh(request):
    '''Refresh access token.'''

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': request.session.get('tokens').get('refresh_token'),
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    res = requests.post(
        url = "https://accounts.spotify.com/api/token", auth=(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET), data=payload, headers=headers
    )
    res_data = res.json()
    print(res_data)
    # Load new token into session
    request.session['tokens']['access_token'] = res_data.get('access_token')

    return json.dumps(request.session['tokens'])



def profile(request):
    # user is logged in
    try:
        auth_code = request.session['auth_code']
        tokens = request.session['tokens']
    # user hasn't logged in
    except:
        return HttpResponseRedirect("/login")
    print(auth_code)
    
    sp = spotipy.Spotify(tokens['access_token'])
    try:
        sp.current_user()
    # token expired NEED TO HANDLE THIS IN MORE SPOTS
    except:
        refresh(request)
        sp = spotipy.Spotify(tokens['access_token'])
        sp.current_user()
    
    try:
        img_url = sp.current_user()['images'][0]['url']
    except:
        img_url =  'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'

    print(img_url)
    # total = []
    # results = sp.current_user_saved_tracks(limit=50)
    # print(results)
    # next = next_offset(results)
    
    # total.append(results)
    # while next and next < int(results['total']):
    #     next_50 = sp.current_user_saved_tracks(limit=50, offset=next)
    #     next = next_offset(next_50)
    #     total.append(next_50)
    #     print(next)
    # tracks = []
    # for r in total:
    #     for track in r['items']:
    #         tracks.append(track)
    return render(request, 'profile.html', {'user':sp.current_user(), 'profile_pic':img_url})

def logout(request):
    # request.session['auth_code'] = None
    # request.session['tokens'] = None
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    
    del request.session['auth_code']
    del request.session['tokens']
    keys = []
    for key in request.session.keys():
        
        keys.append(key)
    for key in keys:
        del request.session[key]
    if(len(request.session.keys()) == 0):
        print("All session keys deleted")
        print("User logged out")
    return HttpResponseRedirect('/profile')

def book_selector(request):
    # request.session.flush()
    print("request", request.GET)
    try:
        auth_code = request.session['auth_code']
        tokens = request.session['tokens']
        print("authcode 1: ", auth_code)      
        # if(auth_code is None):
        #     return HttpResponseRedirect("/sign_in")
    except:
        # user hasn't logged in
        if(request.GET.get('code') is None):
            # request.session['auth_code'] = 0
            # auth_code = request.session['auth_code']
            return HttpResponseRedirect("/login")
        # first time user is logging in
        else:    
            request.session['auth_code'] =  request.GET.get('code')
            auth_code = request.session['auth_code']
            url = "https://accounts.spotify.com/api/token"
            data = {
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': SPOTIPY_REDIRECT_URI,
            }
            res = requests.post(url, auth=(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET), data = data)
            res_data = res.json()
            print(res_data)
            if res_data.get('error') or res.status_code != 200:
                app.logger.error(
                    'Failed to receive token: %s',
                    res_data.get('error', 'No error information received.'),
                )
                abort(res.status_code)

            # Load tokens into session
            request.session['tokens'] = {
                'access_token': res_data.get('access_token'),
                'refresh_token': res_data.get('refresh_token'),
            }
           
        print("authcode 2: ", auth_code)
    print(request.session['tokens'])
    books = Book.objects.all()
    books = books.order_by('bookRank').reverse()
    return render(request, 'book_selector.html', {'books' : books})
   
   
def book_import(request):
    return render (request, 'book_import.html')

# Get list of emotions and clean up the array for chart display
def get_book(request, *args, **kwargs):
    book = Book.objects.filter(bookID = kwargs["id"])[0]
    emotionDict = book.bookEmotion
    pattern = r'[{}]'
    # Remove unwanted characters from emotionDict
    emotionDict = re.sub(pattern, '', emotionDict)
    
    # emotionDict = emotionDict.replace("{","").replace("}","")
    emotionDictStr = emotionDict.split(",")
    emotionDict = {'anticipation': 0.0, 'fear': 0.0, 'anger': 0.0, 'trust': 0.0, 'surprise': 0.0, 'positive': 0.0, 'negative': 0.0, 'sadness': 0.0, 'disgust': 0.0, 'joy': 0.0}
    for emo in emotionDictStr:
        emo = emo.split(":")
        emo[0] = emo[0].replace("'","").replace(" ","")
        # print(emo)
        emotionDict[emo[0]] = float(emo[1])
    # print(emotionDict.keys())
    
    # emotionDict = {}
    # if request.method == 'GET':
        
    response = JsonResponse({'emotionDict':emotionDict})
    return response


@csrf_exempt
def book_import_upload(request):
    form_error = "Submission successful"
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        # text = request.POST.get('text')
        text = request.FILES['text']
        # print(text)
        
        checkBook = Book.objects.filter(title = title)
        
        if(checkBook.count() != 0):
            print("Book Already Exists")
            form_error = "Book Already Exists"
        else:
            # book.bookEmotion = classify_emotion(book)
            book = Book.objects.create()
            book.title = title
            book.author = author
            book.bookText = text
            book.bookID = findID()
            book.save()
        
        
    else:
        form_error = "Submission failed"
        response = JsonResponse({'form_error': form_error})
        return  response  
    response = JsonResponse({'form_error': form_error})
    return  response      

@csrf_exempt
def rank(request):
    
    if request.method == "POST":
        rank_type = request.POST.get('rank_type')
        book_id = request.POST.get('book_id')
        book = Book.objects.get(bookID = book_id)
        print("\nrank type ",rank_type)
        try:
            rank = request.session['rank'+book_id]
            print("\nbook already ranked" ,book.bookRank)
            form_error = "failed"
            response = JsonResponse({'form_error': form_error})
            return  response
        except:
            request.session['rank'+book_id] = 1
            if (rank_type == "upvote"):
                book.bookRank = int(book.bookRank) + 1
                
                book.save()
                print("\nbook rank upvote " ,book.bookRank)
            elif(rank_type == "downvote"):
                book.bookRank = int(book.bookRank) - 1
                book.save()
                print("\nbook rank downvote" ,book.bookRank)
        
            form_error = "successful"
            response = JsonResponse({'form_error': form_error})
            return  response
            
            
            # form_error = "Submission successful"
            # response = JsonResponse({'form_error': form_error})
            # return HttpResponseRedirect('/book_info/'+book_id)

    form_error = ""
    response = JsonResponse({'form_error': form_error})
    return  response 

def findID():
    newID = 65000
    while(Book.objects.filter(bookID = newID).count() != 0):
        newID += 1
    # print(newID)
    return newID

@csrf_exempt
def book_upload(request):
    if request.method == 'POST':
        bookID = request.POST.get('id')
        title = request.POST.get('title')
        author = request.POST.get('author')
        textURL = request.POST.get('text')
        cover = request.POST.get('cover')
        # print(bookID)
        # print(title)
        # print(author)
        # print(textURL)
        checkBook = Book.objects.filter(title = title)
        if(checkBook.count() != 0):
            print("book already exists")
            form_error = "Book Already Exists"
            response = JsonResponse({'form_error': form_error})
            return  response 
        else: 
            book = Book.objects.create()
            book.bookID = bookID
            book.title = title
            book.author = author
            # print(cover)

            img_data = requests.get(cover).content
            f = open('media/coverImages/'+author.replace(" ", "").replace(",","")+'.jpeg', 'wb')
            f.write(img_data)
            f.close()
        
            book.coverImage = 'coverImages/'+author.replace(" ", "").replace(",","")+'.jpeg'
        
            
            if('.zip' in textURL):
                # print("CONTAINS ZIP")
                # print(textURL)
                r = requests.get(textURL)
                f = open('media/books/'+author.replace(" ", "").replace(",","")+'.zip', "wb")
                f.write(r.content)
                f.close()
                r = requests.get(textURL)
                zf = ZipFile('media/books/'+author.replace(" ", "").replace(",","")+'.zip', 'r')
                zf.extractall('media/books/')
                zf.close()
                filename = textURL.replace("http://www.gutenberg.org/files/"+bookID+"/", "media/books/").replace(".zip",".txt")
                # print(filename)
                f = open(filename, "r")
                myfile = File(f)
                book.bookText = myfile
            else:
                r = requests.get(textURL)
                f = open('media/books/'+author.replace(" ", "").replace(",","")+'.txt', "wb")
                f.write(r.content)
                f.close()
                f = open('media/books/'+author.replace(" ", "").replace(",","")+'.txt', "r")
                myfile = File(f)
                book.bookText = "books/"+author.replace(" ", "").replace(",","")+'.txt'
            # book.bookEmotion = classify_emotion(book)
            book.save()
        
       
    form_error = "Submission successful"
    response = JsonResponse({'form_error': form_error})
    return  response 

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


# TODO create ebook reader

# Classifying the emotion of the book
def classify_emotion(book):
     # book = Book.objects.create()

    # Extract the book text
    # book = Book.objects.all().get(pk = kwargs["id"])
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

# Counting the words in the book
def count_words(book):
    numOfWords = 0

    bookText = book.bookText
    # print(bookText)
    bookText.open(mode='r')
    text = bookText.read()
    bookText.close()

    # Tokenize the words and get length of the array of words
    numOfWords = len(text.split())

    book.wordCount = numOfWords
    book.save()

# Get the book information
def book_info(request, *args, **kwargs):
    # book = Book.objects.create()
    # Extract the book text
    book = Book.objects.filter(bookID = kwargs["id"])[0]
    # Classify the emotion if not classified already
    if(book.bookEmotion == ""):
        classify_emotion(book)
    # Count words if not counted already
    count_words(book)

    # auth code
    # user is logged in
    try:
        auth_code = request.session['auth_code']
        tokens = request.session['tokens']
    # user hasn't logged in
    except:
        return HttpResponseRedirect("/login")
    print(auth_code)
    
    sp = spotipy.Spotify(tokens['access_token'])
    try:
        sp.current_user()
    # token expired NEED TO HANDLE THIS IN MORE SPOTS
    except:
        refresh(request)
        sp = spotipy.Spotify(tokens['access_token'])
        sp.current_user()
    # top_arists = aggregate_top_artists(sp)
    # top_tracks = aggregate_top_tracks(sp, top_arists)
    # track_features = get_track_features(sp, top_tracks)
    # calculate_top_top_tracks(book.bookEmotion, track_features, book_title)
    return render(request, 'book_stats.html', {"book":book})

def calculate_top_top_tracks(book_emotions, song_features, book_title):

    book_emotions = format_book_emotion_dict(book_emotions)
    spotify_features = format_track_features(song_features)

    pass


def aggregate_top_artists(sp):
    print('...getting your top artists')
    top_artists_name = []
    top_artists_uri = [] 
    ranges = ['short_term', 'medium_term', 'long_term']
    for r in ranges:
        top_artists_all_data = sp.current_user_top_artists(limit=50, time_range= r)
#         print(top_artists_all_data)
        top_artists_data = top_artists_all_data['items']
        for artist_data in top_artists_data:
            if artist_data["name"] not in top_artists_name:
                top_artists_name.append(artist_data['name'])
                top_artists_uri.append(artist_data['uri'])
    return top_artists_uri

def aggregate_top_tracks(sp, top_artists_uri):
    print("...getting top tracks")
    # top_tracks_name = []
    top_tracks_uri = []
    for artist in top_artists_uri:
         top_tracks_all_data = sp.artist_top_tracks(artist)
         top_tracks_data = top_tracks_all_data['tracks']
         for track_data in top_tracks_data:
             # top_tracks_name.append(track_data['name'])
             top_tracks_uri.append(track_data['uri'])
    
    return top_tracks_uri


def get_track_features(sp, top_tracks_uri):
    print("...getting track features")
    selected_tracks_uri = []
    
#     def group(seq, size):
#         return (seq[pos:pos + size] for pos in range(0, len(seq), size))
#     random.shuffle(top_tracks_uri)
    for tracks in top_tracks_uri:
        tracks_all_data = sp.audio_features(tracks)
        for track_data in tracks_all_data:
            selected_tracks_uri.append(track_data)
            # print(track_data)
    return selected_tracks_uri
            
    # print(len(top_tracks_uri))
    # print(len(selected_tracks_uri))

def format_book_emotion_dict(book_emotion):
    result = {}
    book_emotion.pop('positive')
    book_emotion.pop('negative')
    three_largest = nlargest(3, d, key=d.get)
    for val in three_largest:
        result[val] = book_emotion[val]
        
    return result


def format_track_features(track_features):
    for track in track_features:
        track.pop('key')
        track.pop('loudness')
        track.pop('speechiness')
        track.pop('acousticness')
        track.pop('instrumentalness')
        track.pop('liveness')
        track.pop('tempo')
        track.pop('mode')
        track.pop('type')
        track.pop('time_signature')
        track.pop('duration_ms')
        track.pop('id')
        track.pop('uri')
        track.pop('analysis_url')
    return track_features   

def initial_sign_in(request):
    return render(request, 'initial_sign_in.html')

def sign_in(request):
    # try:
    #     token = prompt_for_user_token('ty_pow', None, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    # except:
    #     os.remove(f".cache-{username}")
    #     token = prompt_for_user_token('ty_pow', None, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, username = username)
    # # token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    # # token = util.prompt_for_user_token('ty_pow', scope)
    # # print(token)
    # # token = prompt_for_user_token('ty_pow', None, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    token_info = sp_oauth.get_cached_token()
    print(token_info)
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(auth_url)
        return HttpResponseRedirect(auth_url)
    # sp = spotipy.Spotify(auth=token_info['access_token'])

    # total = []
    # results = sp.current_user_saved_tracks(limit=50)
    # next = next_offset(results)
    
    # total.append(results)
    # while next and next < int(results['total']):
    #     next_50 = sp.current_user_saved_tracks(limit=50, offset=next)
    #     next = next_offset(next_50)
    #     total.append(next_50)
    #     print(next)
    # tracks = []
    # for r in total:
    #     for track in r['items']:
    #         tracks.append(track)

    return render(request, 'sign_in.html')


def find_books(request):
    return render(request, 'find_books.html')