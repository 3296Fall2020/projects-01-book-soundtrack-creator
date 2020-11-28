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
from zipfile import ZipFile
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
import re
# Create your views here.

scope = 'user-library-read'
SPOTIPY_CLIENT_ID = '1d19391e82ac405fb02f35ebf74cc767'
SPOTIPY_CLIENT_SECRET = '156400e3d8834a8395aaf95d420bb215'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/book_selector/'
username = ''

def index(request):
    return render(request, 'home.html')

def test(request):
    count = 1
    requests_response = requests.get("http://127.0.0.1:8000/find_books/")
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
    
def book_selector(request):
    books = Book.objects.all()
    return render(request, 'book_selector.html', {'books' : books})
   
   
def book_import(request):
    return render (request, 'book_import.html')

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
        print(emo)
        emotionDict[emo[0]] = float(emo[1])
    print(emotionDict.keys())
    
    # emotionDict = {}
    # if request.method == 'GET':
        
    response = JsonResponse({'emotionDict':emotionDict})
    return  response  


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

def findID():
    newID = 65000
    while(Book.objects.filter(bookID = newID).count() != 0):
        newID += 1
    print(newID)
    return newID

@csrf_exempt
def book_upload(request):
    if request.method == 'POST':
        bookID = request.POST.get('id')
        title = request.POST.get('title')
        author = request.POST.get('author')
        textURL = request.POST.get('text')
        cover = request.POST.get('cover')
        print(bookID)
        print(title)
        print(author)
        print(textURL)
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
            print(cover)

            img_data = requests.get(cover).content
            f = open('media/coverImages/'+author.replace(" ", "").replace(",","")+'.jpeg', 'wb')
            f.write(img_data)
            f.close()
        
            book.coverImage = 'coverImages/'+author.replace(" ", "").replace(",","")+'.jpeg'
        
            
            if('.zip' in textURL):
                print("CONTAINS ZIP")
                print(textURL)
                r = requests.get(textURL)
                f = open('media/books/'+author.replace(" ", "").replace(",","")+'.zip', "wb")
                f.write(r.content)
                f.close()
                r = requests.get(textURL)
                zf = ZipFile('media/books/'+author.replace(" ", "").replace(",","")+'.zip', 'r')
                zf.extractall('media/books/')
                zf.close()
                filename = textURL.replace("http://www.gutenberg.org/files/"+bookID+"/", "media/books/").replace(".zip",".txt")
                print(filename)
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
    
    
def book_info(request, *args, **kwargs):
    # book = Book.objects.create()
    # Extract the book text
    book = Book.objects.filter(bookID = kwargs["id"])[0]
    if(book.bookEmotion == ""):
        classify_emotion(book)
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
    results = sp.current_user()
    return render(request, 'sign_in.html')


    

def find_books(request):
    return render(request, 'find_books.html')