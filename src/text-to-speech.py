from gtts import gTTS
import os


def text2speech(mytext):
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("speech.mp3")
    os.system("start welcome.mp3")

mytext = 'Metformin'
text2speech(mytext)

