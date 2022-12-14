import sense_hat, random, time
import rhasspy as rhasspy
from src.utils.colors import R,W,O,Y,N,G,O,S,B

sense = sense_hat.SenseHat()


def plus_sign():
    light = [
    N, N, N, W, W, N, N, N, 
    N, N, N, W, W, N, N, N,
    N, N, N, W, W, N, N, N, 
    W, W, W, W, W, W, W, W,
    W, W, W, W, W, W, W, W,
    N, N, N, W, W, N, N, N,
    N, N, N, W, W, N, N, N,
    N, N, N, W, W, N, N, N,
    ]
    return light

def xred():
    light = [
    R, R, W, W, W, W, R, R, 
    R, R, R, W, W, R, R, R,
    W, R, R, R, R, R, R, W, 
    W, W, R, R, R, R, W, W,
    W, W, R, R, R, R, W, W,
    W, R, R, R, R, R, R, W,
    R, R, R, W, W, R, R, R,
    R, R, W, W, W, W, R, R,
    ]
    return light


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

def backarrow():
    arrow=[N,N,N,W,W,N,N,N,
N,N,W,W,W,W,N,N,
N,W,N,W,W,N,W,N,
W,N,N,W,W,N,N,W,
N,N,N,W,W,N,N,N,
N,N,N,W,W,N,N,N,
N,N,N,W,W,N,N,N,
N,N,N,W,W,N,N,N]
    return arrow



menu = { 
        "picks" : (plus_sign(), xred(), backarrow()),
        "choice_index" : 0,
        }

def display(state) :
    if(state["choice_index"] == 3) :
        state["choice_index"] = 0
    elif (state["choice_index"] == -1) :
        state["choice_index"] = 2
    sense.set_pixels(state["picks"][state["choice_index"]])


def add_list() :
    f = open("/home/pi/APP3/src/db/courses.txt", 'r+')

    sense.set_pixels(sounds_light())
    while True :
        f.seek(0)
        course_list = f.read().split("\n")
        print(course_list)
    
        intent = rhasspy.speech_to_intent()
        if(intent["name"] == "leave") :
            break
        if(intent["name"] == "list") :
            rhasspy.text_to_speech("Il y a dans votre liste : ")
            for alim in course_list :
                rhasspy.text_to_speech(alim)
            return
        if(intent["name"] == "ajouter" and not course_list.count(intent["variables"]["aliments"])) :
            f.write(str(intent["variables"]["num"]) + " " + intent["variables"]["aliments"] + '\n')
            f.flush()

def courses() :
    sense.clear()
    f = open("/home/pi/APP3/src/db/courses.txt", 'r+')

    while True:
        events = sense.stick.get_events()
        if events:
            for event in events:
                if event.action != 'pressed':
                    #this is a hold or keyup; move on
                    continue
                if event.direction == 'left':
                    menu["choice_index"] += 1
                elif event.direction == 'right':
                    menu["choice_index"] -= 1
                elif event.direction == 'middle':
                    # User picks selected option
                    if(menu["choice_index"] == 0) :
                        add_list()
                    if(menu["choice_index"] == 1) :
                        f.truncate(0)
                    if(menu["choice_index"] == 2) :
                        return
        display(menu)


    






