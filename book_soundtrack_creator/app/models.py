from django.db import models
from emotion_classifier_nrclex import *

# Create your models here.

class Book(models.Model): 
    title = models.CharField(verbose_name = "Book Title", 
                                max_length = 255, blank = False)
    wordCount = models.CharField(verbose_name = "Number of words", max_length = 255, blank = False)
    bookText = models.FileField(verbose_name = "Book text" , upload_to = 'books/')

    # Call emotion classifier and analyze bookText (TO-DO: Figure out type of field (dictionary) and check correctness of algorithm)
    emotion = emotion_classifier(bookText)  # emotion is a dictionary of {emotion: value}
    bookEmotion = models.CharField(verbose_name = "Emotion", max_length = 100000, blank = False)    # Should store dictionary


class User(models.Model):
    email = models.CharField(verbose_name = "User Email", max_length = 255, blank = False)
    userId = models.CharField(verbose_name = "Spotify user id", max_length = 255, blank = False)
    name = models.CharField(verbose_name = "Spotify display name", max_length = 255, blank = True)
    # profilePic = models.
    # password?




