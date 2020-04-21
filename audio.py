import speech_recognition as sr     # import the library

google_api_key = "AIzaSyDj4SHN7pggP4JVZfqXJ_R4G4-ZbQWaPlU"


def stt():
    r = sr.Recognizer()                 # initialize recognizer
    with sr.Microphone() as source:     # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)        # listen to the source
        try:
            text = r.recognize_google(audio, language='it-IT')    # use recognizer to convert our audio into text part.
            #text = r.recognize_google_cloud(audio, language='it-IT', key=google_api_key)    # use recognizer to convert our audio into text part.
            print("You said : {}".format(text))
            return text
        except Exception as e: 
            print(e)
            print("Sorry could not recognize your voice")    # In case of voice not recognized  clearly
            return None