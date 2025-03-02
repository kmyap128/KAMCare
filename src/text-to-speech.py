import sys
from gtts import gTTS
import os


def text2speech(mytext):
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("speech.mp3")
    os.system("start speech.mp3")

# mytext = 'Metformin'
# text2speech(mytext)

def main():
    # Check if the script is being called with an argument (text to convert to speech)
    if len(sys.argv) > 1:
        mytext = sys.argv[1]  # The first argument passed (text for speech)
        text2speech(mytext)
    else:
        print("No text provided.")

if __name__ == "__main__":
    main();