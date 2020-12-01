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

scope = 'user-library-read user-top-read user-follow-read playlist-modify-public playlist-modify-private'
SPOTIPY_CLIENT_ID = '1d19391e82ac405fb02f35ebf74cc767'
SPOTIPY_CLIENT_SECRET = '156400e3d8834a8395aaf95d420bb215'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/book_selector/'
username = ''
CACHE = '.spotipyoauthcache'

# Serves homepage and starts user session
def index(request):
    try:
        user = request.session['user']
    except:
        request.session['user'] = randint(0, 100)
        user = request.session['user']
    return render(request, 'home.html',{'user':user})

# test view (used this to develop some experimental functionality)
def test(request):
    count = 1
    requests_response = requests.get("http://127.0.0.1:8000/find_books/")
    try:
        user = request.session['user']
    except:
        request.session['user'] = randint(0, 100)
    # print("User " +str(request.session['user'])+": "+requests_response.content)
    # r = requests.get("http://gutendex.com/books/"+str(count)).json()
    # authors = set()
    # print("User " +str(request.session['user'])+": "+'id' in r)
    # while(count < 67000):
        
    #     if(len(r['authors']) > 0):
    #         # for a in r['authors']  :
    #         print("User " +str(request.session['user'])+": "+r['authors'][0]['name'] + " " +str(count))    
    #         authors.add(r['authors'][0]['name'])
    #     count +=1
    #     r = requests.get("http://gutendex.com/books/"+str(count)).json()
    #     if(count % 100 == 0):
    #         print("User " +str(request.session['user'])+": "+str(count/65000) + "%")
    #     while(not('authors' in r)):
    #         print("User " +str(request.session['user'])+": "+"missing response! " + str(count))
    #         count += 1
    #         r = requests.get("http://gutendex.com/books/"+str(count)).json()

    # print("User " +str(request.session['user'])+": "+authors)
    # while(requests.get("https://www.gutenberg.org/books/"+count)
    # requests_response = requests.get("https://www.gutenberg.org/browse/authors/a")
    # print("User " +str(request.session['user'])+": "+requests_response)
    soup = BeautifulSoup(requests_response, 'html.parser')
    # bookshelf = soup.find_all('li')
    # print("User " +str(request.session['user'])+": "+"hellooooo" ,bookshelf)
    # print("User " +str(request.session['user'])+": "+soup)
    django_response = HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )
    # print("User " +str(request.session['user'])+": "+django_response.content)
    return django_response
    
# TODO this is no longer needed
# Serves login page 
def login(request):
    return render(request, 'login.html')

# Called when the spotify access token is expired
# called in get_spotify
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
    # print("User " +str(request.session['user'])+": "+res_data)
    # Load new token into session
    request.session['tokens']['access_token'] = res_data.get('access_token')

    return json.dumps(request.session['tokens'])

# checks if the spotify access token is good
# returns the spotipy.Spotify object
def get_spotify(request):
    auth_code = request.session['auth_code']
    tokens = request.session['tokens']
    sp = spotipy.Spotify(tokens['access_token'])
    try:
        sp.current_user()
    # token expired NEED TO HANDLE THIS IN MORE SPOTS
    except:
        refresh(request)
        sp = spotipy.Spotify(tokens['access_token'])
        sp.current_user()
    sp = spotipy.Spotify(tokens['access_token'])
    return sp

# serves profile page if the user is logged in
def profile(request):
    # user is logged in
    try:
        auth_code = request.session['auth_code']
        tokens = request.session['tokens']
    # user hasn't logged in
    except:
        request.session['url'] = "/profile"
        return HttpResponseRedirect("/login")
    sp = get_spotify(request)
    
    try:
        img_url = sp.current_user()['images'][0]['url']
    except:
        img_url =  'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'

    # print("User " +str(request.session['user'])+": "+img_url)
    # total = []
    # results = sp.current_user_saved_tracks(limit=50)
    # print("User " +str(request.session['user'])+": "+results)
    # next = next_offset(results)
    
    # total.append(results)
    # while next and next < int(results['total']):
    #     next_50 = sp.current_user_saved_tracks(limit=50, offset=next)
    #     next = next_offset(next_50)
    #     total.append(next_50)
    #     print("User " +str(request.session['user'])+": "+next)
    # tracks = []
    # for r in total:
    #     for track in r['items']:
    #         tracks.append(track)
    return render(request, 'profile.html', {'user':sp.current_user(), 'profile_pic':img_url})

# logs the user out of our app by deleting all session keys
# returns to home page
def logout(request):
    # request.session['auth_code'] = None
    # request.session['tokens'] = None
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    print("\n\n\n++++++++++++++++User " +str(request.session['user'])+" LOGGING OUT+++++++++++++++++++++++")
    del request.session['auth_code']
    del request.session['tokens']
    keys = []
    for key in request.session.keys():
        keys.append(key)
    print("User " +str(request.session['user'])+": "+"LOGOUT -- session keys: ",keys)
    for key in keys:
        del request.session[key]
    if(len(request.session.keys()) == 0):
        print("LOGOUT: All session keys deleted")
        print("LOGOUT: User logged out")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n\n")
        
    return HttpResponseRedirect('/')

# acts as the main redirect page after spotify log in
# also serves popular books in order
def book_selector(request):
    # print("User " +str(request.session['user'])+": "+"request", request.GET) #prints auth code from spotify
    # print("User " +str(request.session['user'])+": "+request.session['url']) # prints redirect url key from session
    
    # checks if users have already logged in
    try:
        auth_code = request.session['auth_code']
        tokens = request.session['tokens']
    # prompts user to login to spotify or logs them into app if redirected from spotify
    except:
        # user hasn't logged in and wants to access the book selector page
        if(request.GET.get('code') is None):
            request.session['url'] = "/book_selector"
            return HttpResponseRedirect("/login")

        # first time user is logging in
        # this means that the user just got redirected from spotify
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
            # print("User " +str(request.session['user'])+": "+res_data)
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
            sp = get_spotify(request)
            print("User " +str(request.session['user'])+": "+"\n\n++++++++++++++++++++++++++++++++++++++++++++++NEW USER LOGGED IN+++++++++++++++++++++++++++++++++++++++++++++\n\n"
                        +str(sp.current_user())+
                  "\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
            
            if(request.session['url'] != "/book_selector"):
                return HttpResponseRedirect(request.session['url'])

        # print("User " +str(request.session['user'])+": "+"authcode 2: ", auth_code)
    # print("User " +str(request.session['user'])+": "+"book_selector -- tokens from spotify: ",request.session['tokens'])
    books = Book.objects.all()
    books = books.order_by('bookRank').reverse()[:10] #reverse ranks books
    return render(request, 'book_selector.html', {'books' : books})
   
   
def book_import(request):
    return render (request, 'book_import.html')

def createPlaylist(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        # if user has created a playlist for this book
        try:
            book_id = request.POST.get('book_id')
            playlist = request.session['playlist'+book_id]
            form_error = "USER ALREADY CREATED THIS PLAYLIST"
            print("User " +str(request.session['user'])+": "+"rank -- POST message: ", form_error)
            form_error = "failed"
            response = JsonResponse({'form_error': form_error})
            return  response
         # if user has created a playlist for this book
        except:
            request.session['playlist'+book_id] = 1  
            print(book_id)
            book = Book.objects.get(bookID = book_id)
            sp = get_spotify(request)
            try:
                top_artists = aggregate_top_artists(sp)
                top_tracks = aggregate_top_tracks(sp, top_artists)
                track_features = get_track_features(sp, top_tracks)
                calculate_top_tracks(sp, book.bookEmotion, track_features, book.title)
                form_error = "successful"
                response = JsonResponse({'form_error': form_error})
                return  response
            except:
                form_error = "failed no history"
                response = JsonResponse({'form_error': form_error})
                return  response
              
    else:
        form_error = "Submission failed"
        response = JsonResponse({'form_error': form_error})
        return  response  

@csrf_exempt
def book_import_upload(request):
    if request.method == 'POST':
        form_error = "Form recieved"
        print("User " +str(request.session['user'])+": "+"book_import_upload -- POST message: ", form_error)
        title = request.POST.get('title')
        author = request.POST.get('author')
        # text = request.POST.get('text')
        text = request.FILES['text']
        # print("User " +str(request.session['user'])+": "+text)
        
        checkBook = Book.objects.filter(title = title)
        # checks if book exists
        if(checkBook.count() != 0):
            print("User " +str(request.session['user'])+": "+"BOOK_IMPORT_UPLOAD: Book Already Exists")
            form_error = "Book Already Exists"
            print("User " +str(request.session['user'])+": "+"book_import_upload -- POST message: ", form_error)
        # book does not exist so create it
        else:
            # book.bookEmotion = classify_emotion(book)
            book = Book.objects.create()
            book.title = title
            book.author = author
            book.bookText = text
            book.bookID = findID()
            book.save()  
            form_error = "Book Created"
            print("User " +str(request.session['user'])+": "+"book_import_upload -- POST message: ", form_error)   
    else:
        form_error = "Submission failed"
        response = JsonResponse({'form_error': form_error})
        return  response  
    response = JsonResponse({'form_error': form_error})
    return  response      

# creates ID for manually imported book
# called by book_import_upload
def findID():
    newID = 65000
    while(Book.objects.filter(bookID = newID).count() != 0):
        newID += 1
    # print("User " +str(request.session['user'])+": "+newID)
    return newID


@csrf_exempt
def book_upload(request):
    if request.method == 'POST':
        form_error = "Form recieved"
        print("User " +str(request.session['user'])+": "+"book_import_upload -- POST message: ", form_error)
        bookID = request.POST.get('id')
        title = request.POST.get('title')
        author = request.POST.get('author')
        textURL = request.POST.get('text')
        cover = request.POST.get('cover')
        # print("User " +str(request.session['user'])+": "+bookID)
        # print("User " +str(request.session['user'])+": "+title)
        # print("User " +str(request.session['user'])+": "+author)
        # print("User " +str(request.session['user'])+": "+textURL)
        checkBook = Book.objects.filter(title = title)
        if(checkBook.count() != 0):
            print("User " +str(request.session['user'])+": "+"BOOK_UPLOAD: book already exists")
            form_error = "Book Already Exists"
            print("User " +str(request.session['user'])+": "+"book_upload -- POST message: ", form_error)
            response = JsonResponse({'form_error': form_error})
            return  response 
        else: 
            book = Book.objects.create()
            book.bookID = bookID
            book.title = title
            book.author = author
            # print("User " +str(request.session['user'])+": "+cover)
            img_data = requests.get(cover).content
            f = open('media/coverImages/'+author.replace(" ", "").replace(",","")+'.jpeg', 'wb')
            f.write(img_data)
            f.close()
            book.coverImage = 'coverImages/'+author.replace(" ", "").replace(",","")+'.jpeg'
        
            # if book in zip download and unzip file
            # then load in book text
            if('.zip' in textURL):
                # print("User " +str(request.session['user'])+": "+"CONTAINS ZIP")
                # print("User " +str(request.session['user'])+": "+textURL)
                r = requests.get(textURL)
                f = open('media/books/'+author.replace(" ", "").replace(",","")+'.zip', "wb")
                f.write(r.content)
                f.close()
                r = requests.get(textURL)
                zf = ZipFile('media/books/'+author.replace(" ", "").replace(",","")+'.zip', 'r')
                zf.extractall('media/books/')
                zf.close()
                filename = textURL.replace("http://www.gutenberg.org/files/"+bookID+"/", "media/books/").replace(".zip",".txt")
                # print("User " +str(request.session['user'])+": "+filename)
                f = open(filename, "r")
                myfile = File(f)
                book.bookText = myfile
            # load in book text
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
            form_error = "Book Created"
            print("User " +str(request.session['user'])+": "+"book_upload -- POST message: ", form_error)
       
    form_error = "Submission successful"
    response = JsonResponse({'form_error': form_error})
    return  response 

@csrf_exempt
def rank(request):  
    if request.method == "POST":
        form_error = "Form recieved"
        print("User " +str(request.session['user'])+": "+"rank -- POST message: ", form_error)
        rank_type = request.POST.get('rank_type')
        book_id = request.POST.get('book_id')
        book = Book.objects.get(bookID = book_id)
        # print("User " +str(request.session['user'])+": "+"\nrank type ",rank_type)
        try:
            rank = request.session['rank'+book_id]
            # print("User " +str(request.session['user'])+": "+"\nbook already ranked" ,book.bookRank)
            form_error = "USER ALREADY VOTED THIS SESSION"
            print("User " +str(request.session['user'])+": "+"rank -- POST message: ", form_error)
            form_error = "failed"
            response = JsonResponse({'form_error': form_error})
            return  response
        except:
            request.session['rank'+book_id] = 1
            if (rank_type == "upvote"):
                book.bookRank = int(book.bookRank) + 1
                book.save()
                form_error = "successful"
                print("User " +str(request.session['user'])+": "+"rank -- upvote: ", form_error)
                # print("User " +str(request.session['user'])+": "+"\nbook rank upvote " ,book.bookRank)
            elif(rank_type == "downvote"):
                book.bookRank = int(book.bookRank) - 1
                book.save()
                form_error = "successful"
                print("User " +str(request.session['user'])+": "+"rank -- upvote: ", form_error)
                # print("User " +str(request.session['user'])+": "+"\nbook rank downvote" ,book.bookRank)
        
            form_error = "successful"
            response = JsonResponse({'form_error': form_error})
            return  response
    else:
        form_error = "RANK FAILED"
        print("User " +str(request.session['user'])+": "+"rank: ", form_error)
        response = JsonResponse({'form_error': form_error})
        return  response 

# Classifying the emotion of the book
# called by book_info
def classify_emotion(book):
    bookText = book.bookText
    bookText.open(mode='r')
    lines = bookText.readlines()
    bookText.close()
    
    # Call emotion classifier and analyze bookText (TO-DO: Figure out type of field (dictionary) and check correctness of algorithm)
    emotion = Book.emotion_classifier(lines)  # Returns a dictionary of {emotion: value}
    # print("User " +str(request.session['user'])+": "+"classify_emotion: ", emotion)
    book.bookEmotion = emotion
    book.save()

# Counting the words in the book
# called by book_info
def count_words(book):
    numOfWords = 0

    bookText = book.bookText
    # print("User " +str(request.session['user'])+": "+bookText)
    bookText.open(mode='r')
    text = bookText.read()
    bookText.close()

    # Tokenize the words and get length of the array of words
    numOfWords = len(text.split())

    book.wordCount = numOfWords
    book.save()

# Get list of emotions and clean up the array for chart display
# called by book_info
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
        # print("User " +str(request.session['user'])+": "+emo)
        emotionDict[emo[0]] = float(emo[1])
    # print("User " +str(request.session['user'])+": "+"get_book -- dictionary keys: ", emotionDict.keys())
    
    response = JsonResponse({'emotionDict':emotionDict})
    return response

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
    # print("User " +str(request.session['user'])+": "+auth_code)
    
    sp = spotipy.Spotify(tokens['access_token'])
    try:
        sp.current_user()
    # token expired NEED TO HANDLE THIS IN MORE SPOTS
    except:
        refresh(request)
        sp = spotipy.Spotify(tokens['access_token'])
        sp.current_user()
    # top_artists = aggregate_top_artists(sp)
    # top_tracks = aggregate_top_tracks(sp, top_artists)
    # track_features = get_track_features(sp, top_tracks)
    # calculate_top_tracks(sp, book.bookEmotion, track_features, book.title)
    return render(request, 'book_stats.html', {"book":book})

def calculate_top_tracks(sp, book_emotions, song_features, book_title):
    print("...calculating tracks")
    book_emotions = format_book_emotion_dict(book_emotions)
    spotify_features = format_track_features(song_features)


    book_score = calculate_book_score(book_emotions)
    tracks = calculate_books(book_score, spotify_features)
    # print(book_score)
    # print(tracks)

    # create new playlist
    new_playlist = sp.user_playlist_create(sp.current_user()['id'], name=book_title, public=True, collaborative=False, description='')
    # load songs into new playlist
    sp.user_playlist_add_tracks(sp.current_user()['id'], new_playlist['id'], tracks=tracks, position=None)

    pass

def calculate_books(book_score, track_features):
    tracks = []
    temp_dict = {}
    for track in track_features:
        temp_dict[abs(track['valence'] - book_score)] = track['id']

        i = 0
    for score in sorted(temp_dict.keys()):
        tracks.append(temp_dict[score])
        i+=1
        if i >= 30:
            break
    return tracks

def calculate_book_score(book_emotion_dict):
    count = 0
    for emotion in book_emotion_dict:
        if emotion == 'anticipation':
            count += 0.25
        if emotion == 'joy':
            count += 0.45
        if emotion == 'fear':
            count += 0
        if emotion == 'anger':
            count += 0
        if emotion == 'trust':
            count += .25
        if emotion == 'surprise':
            count += 0.3
        if emotion == 'sadness':
            count += 0
        if emotion == 'disgust':
            count += 0.1
    return count

    
def aggregate_top_artists(sp):
    # print('...getting your top artists')
    top_artists_name = []
    top_artists_uri = [] 
    ranges = ['medium_term']
    for r in ranges:
        top_artists_all_data = sp.current_user_top_artists(limit=20, time_range= r)
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
    book_emotion = eval(book_emotion)
    # print(type(book_emotion))
    # print(book_emotion)
    book_emotion.pop('positive')
    book_emotion.pop('negative')
    three_largest = nlargest(3, book_emotion, key=book_emotion.get)
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
        track.pop('uri')
        track.pop('analysis_url')
    return track_features   

def initial_sign_in(request):
    return render(request, 'initial_sign_in.html')

# redirects user to spotify login
# redirects to book_selector
def sign_in(request):
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, username = username)
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        # print("User " +str(request.session['user'])+": "+auth_url)
        return HttpResponseRedirect(auth_url)
    return render(request, 'sign_in.html')

# serves find books to user
def find_books(request):
    return render(request, 'find_books.html')