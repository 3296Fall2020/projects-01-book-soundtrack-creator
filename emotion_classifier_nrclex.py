# Import required NRCLex modules
from nrclex import NRCLex

# Assign text (example text -- will use text from book input in future)
text = ['hate', 'lovely', 'person', 'worst']

# Iterate through list of words in text
for i in range(len(text)):
    # Create emotion object
    emotion = NRCLex(text[i])

    # Classify emotion of word
    print('\n\n', text[i], ': ', emotion.top_emotions)
