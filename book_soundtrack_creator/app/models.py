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
    bookEmotion = models.CharField(verbose_name = "Book Emotion", max_length = 255)

    @classmethod
    # Create emotion classifier method for Book class
    def emotion_classifier(self, text):
        print("works")
        emotionList = []
        emotionDict = {'anticipation': 0.0, 'fear': 0.0, 'anger': 0.0, 'anticip': 0.0, 'trust': 0.0, 'surprise': 0.0, 'positive': 0.0, 'negative': 0.0, 'sadness': 0.0, 'disgust': 0.0, 'joy': 0.0}
        # Iterate through items in list in text
        for i in range(len(text)):
            # Create emotion object
            emotions = NRCLex(text[i]).top_emotions
            # emotionList.append(emotion.top_emotions)
            for emo in emotions:
                emotionDict[emo[0]] += float(emo[1])
            print(text[i])
            
            # Return list of top emotions from text
            # return emotion.top_emotions
        for emotion in emotionList:
            print(emotion)
        return emotionDict


    def __str__(self):
        return self.title

class User(models.Model):
    email = models.CharField(verbose_name = "User Email", max_length = 255, blank = False)
    userId = models.CharField(verbose_name = "Spotify user id", max_length = 255, blank = False)
    name = models.CharField(verbose_name = "Spotify display name", max_length = 255, blank = True)
    # profilePic = models.
    # password?


