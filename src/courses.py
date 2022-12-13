import sense_hat, random, time
import rhasspy as rhasspy
from src.utils.colors import R,W,O,Y,N,G,O,S,B

sense = sense_hat.SenseHat()

def sounds_light():
    light = [
    N, N, N, N, N, N, N, N, 
    N, N, N, W, N, N, W, N,
    N, N, W, W, N, N, N, W, 
    W, W, W, W, N, W, N, W,
    W, W, W, W, N, W, N, W,
    N, N, W, W, N, N, N, W,
    N, N, N, W, N, N, W, N,
    N, N, N, N, N, N, N, N,
    ]
    return light


def courses() :
    sense.set_pixels(sounds_light())

    f = open("/home/pi/APP3/src/db/courses.txt", 'r+')

    while True :
        f.seek(0)
        course_list = f.read().split("\n")
        print(course_list)
    
        intent = rhasspy.speech_to_intent()
        if(intent["name"] == "leave") :
            break
        if(intent["name"] == "create") :
            f.truncate(0)
        if(intent["name"] == "list") :
            rhasspy.text_to_speech("Il y a dans votre liste : ")
            for alim in course_list :
                rhasspy.text_to_speech(alim)
        if(intent["name"] == "ajouter" and not course_list.count(intent["variables"]["aliments"])) :
            f.write(intent["variables"]["aliments"] + '\n')
            f.flush()






