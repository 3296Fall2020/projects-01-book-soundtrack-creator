# Import required NRCLex modules
from nrclex import NRCLex

# Create emotion classifier method
def emotion_classifier(text):
    # Iterate through items in list in text
    for i in range(len(text)):
        # Create emotion object
        emotion = NRCLex(text[i])
        # Return list of top emotions from text
        return emotion.top_emotions
