from django.db import models
# Import required NRCLex modules
from nrclex import NRCLex

# Create your models here.

class Book(models.Model): 
    title = models.CharField(verbose_name = "Book Title", 
                                max_length = 255, blank = False)
    wordCount = models.CharField(verbose_name = "Number of words", max_length = 255, blank = False)
    bookText = models.FileField(verbose_name = "Book text" , upload_to = 'books/')
    # TO-DO: Not sure what field this should be
    bookEmotion = models.FileField(verbose_name = "Book Emotion" , upload_to = 'emotions/')

    @classmethod
    # Create emotion classifier method for Book class
    def emotion_classifier(text):
        # Iterate through items in list in text
        for i in range(len(text)):
            # Create emotion object
            emotion = NRCLex(text[i])
            # Return list of top emotions from text
            return emotion.top_emotions

class User(models.Model):
    email = models.CharField(verbose_name = "User Email", max_length = 255, blank = False)
    userId = models.CharField(verbose_name = "Spotify user id", max_length = 255, blank = False)
    name = models.CharField(verbose_name = "Spotify display name", max_length = 255, blank = True)
    # profilePic = models.
    # password?


