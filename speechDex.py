"""
based on the game tutorial found here: https://realpython.com/python-speech-recognition/
"""
import time
import json
import speech_recognition as sr
import pyttsx3

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
            successful
    "error":   `None` if no error occured, otherwise a string containing
            an error message if the API could not be reached or
            speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
            otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        #TO DO: control how long mic stays on 
        audio = recognizer.listen(source, phrase_time_limit=10)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    #print("end recording")

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, show_all = True)
        #print(response["transcription"])
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

if __name__ == "__main__":

    GEN1_DEX = {}
    with open("Verbal Pokedex\dexDict.txt") as f:
        for line in f:
            (k, v) = line.split(":")
            GEN1_DEX[k] = int(v)
    #print(GEN1_DEX)


    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()

    instructions = "Say a pokemons name"
    flag = True
    PROMPT_LIMIT=5

    print(instructions)
    engine.say(instructions)
    engine.runAndWait()
    time.sleep(0.5)

    while(flag):
        for j in range(PROMPT_LIMIT):
            print('mic on')
            #TO DO: match up mic coming on with verbal and printed cues
            engine.say("eeep")
            engine.runAndWait()
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")
        
        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        found=False
        i=0
        while i<len(guess["transcription"].get('alternative')) and (not found):
            name_to_test = guess["transcription"].get('alternative')[i].get('transcript').lower()
            # show the user the transcription
            print("You said: {}".format(name_to_test))


            if name_to_test in ["stop","cancel","end","done"]:
                print("stopping")
                engine.say("stopping")
                engine.runAndWait()
                flag=False
                found=True
                break
            else:
                try: 
                    print("{name} is number {id}".format(name=name_to_test,id=GEN1_DEX[name_to_test]))
                    engine.say("{name} is number {id}".format(name=name_to_test,id=GEN1_DEX[name_to_test]))
                    engine.runAndWait()
                    found=True
                    
                except KeyError:
                    print("trying an alternative...")
                    #print("I did not find {}".format(name_to_test))
                    engine.say("trying an alternative...")
                    engine.runAndWait()
                    i=i+1
                    if i==len(guess["transcription"].get('alternative')) :
                        print("try again")
                        engine.say("failed to find pokemon")
                        engine.runAndWait()
                except Exception as e:
                    print(e)
                    print("{} produced an error".format(name_to_test))
                    engine.say("{} produced an error".format(name_to_test))
                    engine.runAndWait()
                    i=i+1
        
        