from django.db import models
# Import required NRCLex modules
from nrclex import NRCLex

# Create your models here.

class Book(models.Model): 
    bookID = models.CharField(verbose_name = "id", max_length = 10, blank = False, default = -1)
    title = models.CharField(verbose_name = "Book Title", 
                                max_length = 255, blank = False)
    author = models.CharField(verbose_name = "Author Name", max_length = 255, blank = True)
    coverImage = models.ImageField(verbose_name = "Cover art", upload_to = 'coverImages/', blank = True)                               
    wordCount = models.CharField(verbose_name = "Number of words", max_length = 255, blank = True)
    bookText = models.FileField(verbose_name = "Book text" , upload_to = 'books/')
    # TO-DO: Not sure what field this should be
    bookEmotion = models.CharField(verbose_name = "Book Emotion", max_length = 255)
    bookEmotionGraph = models.ImageField(verbose_name="Book Bar Graph", upload_to='static/img', default='bookgraphs/blank.png')
    @classmethod
    # Create emotion classifier method for Book class
    def emotion_classifier(self, text):
        print("works")
        emotionList = []
        emotionDict = {'anticipation': 0.0, 'fear': 0.0, 'anger': 0.0, 'trust': 0.0, 'surprise': 0.0, 'positive': 0.0, 'negative': 0.0, 'sadness': 0.0, 'disgust': 0.0, 'joy': 0.0}
        # Iterate through items in list in text
        for i in range(len(text)):
            # Create emotion object
            emotions = NRCLex(text[i]).top_emotions
            # emotionList.append(emotion.top_emotions)
            for emo in emotions:
                if emo[0] == 'anticip':
                    emotionDict['anticipation'] += float(emo[1])
                else:
                    emotionDict[emo[0]] += float(emo[1])
            # print(text[i])
            
            # Return list of top emotions from text
            # return emotion.top_emotions
        max = 0.0
        for emo in emotionDict:
            if(emotionDict[emo] > max):
                max = emotionDict[emo]
        for emo in emotionDict:
            emotionDict[emo] /= max

        return emotionDict


    def __str__(self):
        return self.title


class User(models.Model):
    email = models.CharField(verbose_name = "User Email", max_length = 255, blank = False)
    userId = models.CharField(verbose_name = "Spotify user id", max_length = 255, blank = False)
    name = models.CharField(verbose_name = "Spotify display name", max_length = 255, blank = True)
    # profilePic = models.
    # password?


