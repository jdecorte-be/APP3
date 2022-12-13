import sense_hat, random, time
import rhasspy as rhasspy
from src.utils.colors import R,W,O,Y,N,G,O,S,B
from src.crypto import encode, decode, hashing

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

def joystick():
    light = [
    R, N, N, N, N, N, N, R, 
    N, N, N, W, N, N, W, N,
    N, N, W, W, N, N, N, W, 
    W, W, W, W, N, W, N, W,
    W, W, W, W, N, W, N, W,
    N, N, W, W, N, N, N, W,
    N, N, N, W, N, N, W, N,
    R, N, N, N, N, N, N, R,
    ]
    return light


menu = { 
        "picks" : (sounds_light(), joystick()),
        "choice_index" : 0,
        }

def display(state) :
    if(state["choice_index"] == 2) :
        state["choice_index"] = 0
    elif (state["choice_index"] == -1) :
        state["choice_index"] = 1
    sense.set_pixels(state["picks"][state["choice_index"]])


def launch_voice() :
    sense.set_pixels(sounds_light()) # animate
    code = ""

    while True and len(code) != 4:
        intent = rhasspy.speech_to_intent()
    
        if(intent["name"] == "num") :
            for i in range(4) :
                code += str(intent["variables"]["num" + str(i)])
    return code



def launch_manual() :
    count = 0
    code = ""
    while True and len(code) != 4:
        events = sense.stick.get_events()
        if events:
            for event in events:
                if event.action != 'pressed':
                    #this is a hold or keyup; move on
                    continue
                if event.direction == 'right' and count < 9:
                    count += 1
                elif event.direction == 'left' and count > 0:
                    count -= 1
                elif event.direction == 'middle':
                    # User picks selected option
                    code += str(count)
        sense.show_letter(str(count))
    return code


def password_man() :
    code = ""
    catch_pass = True
    while catch_pass:
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
                        code = launch_voice()
                        catch_pass = False
                    if(menu["choice_index"] == 1) :
                        code = launch_manual()
                        catch_pass = False
        display(menu)
    sense.show_message("Your code is : " + code)
    

    f = open("/home/pi/APP3/src/db/password", 'r+')
    f.truncate(0)
    f.write(encode("sjkdfhjsdkhfksd", code))
    # print (decode("0434", f.read()))



