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
    # rhasspy.train_intent_files("sentences.ini")

    choice = 1
    while True:
        events = sense.stick.get_events()
        if events:
            for event in events:
                if event.action != 'pressed':
                    #this is a hold or keyup; move on
                    continue
                if event.direction == 'right' and choice < 3:
                    choice += 1
                elif event.direction == 'left' and choice > 1:
                    choice -= 1
                elif event.direction == 'middle':
                    sense.set_pixels(sounds_light())
                    f = open("/home/pi/projetAPP03/src/db/courses" + str(choice) + ".txt", "w")

                    while True :
                        intent = rhasspy.speech_to_intent()
                        if(intent["name"] == "leave") :
                            break
                        if(intent["name"] == "create") :
                            f.close()
                        if(intent["name"] == "ajouter") :
                            f.write(intent["variables"]["aliments"] + '\n')
                        
                sense.show_letter(str(choice))
 






