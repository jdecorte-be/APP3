import sense_hat, random, time
import rhasspy as rhasspy
from src.utils.colors import R,W,O,Y,N,G,O,S,B
from src.crypto import encode, decode, hashing

s = sense_hat.SenseHat()

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
    logo = [
    N, N, N, N, N, N, N, N, 
    N, N, N, N, N, N, N, N,
    N, N, W, N, N, W, N, N, 
    N, W, W, N, N, W, W, N,
    W, W, W, N, N, W, W, W,
    N, W, W, N, N, W, W, N,
    N, N, W, N, N, W, N, N,
    N, N, N, N, N, N, N, N,
    ]
    return logo

def interogation():
    light = [
    N, N, W, W, W, W, N, N, 
    N, W, N, N, N, N, W, N,
    N, N, N, N, N, N, W, N, 
    N, N, N, N, W, W, N, N,
    N, N, N, W, W, N, N, N,
    N, N, N, N, N, N, N, N,
    N, N, N, W, W, N, N, N,
    N, N, N, W, W, N, N, N,
    ]
    return light


menu = { 
        "picks" : (interogation(), sounds_light(), joystick()),
        "choice_index" : 0,
        }


"""
Ce code utilise le Sense HAT, une carte d'extension matérielle pour le Raspberry Pi,
pour afficher un menu sur la matrice LED 8x8 du Sense HAT. Le menu comprend trois options :
une interrogation, un signal sonore et un joystick. L'utilisateur peut naviguer dans
le menu en utilisant le joystick du Sense HAT et sélectionner une option en appuyant sur
le joystick. Si l'utilisateur sélectionne l'option de l'interrogation, il peut entrer
un mot de passe à l'aide de la voix ou du joystick, en suivant les instructions affichées
sur la matrice LED. Le mot de passe est ensuite chiffré et enregistré dans un fichier.

Si l'utilisateur sélectionne l'option du signal sonore, il peut entendre les instructions pour
entrer un mot de passe à l'aide de la voix. Si l'utilisateur sélectionne l'option du joystick,
il peut entrer un mot de passe à l'aide du joystick, en suivant les instructions affichées sur
la matrice LED. Le code utilise également les packages Rhasspy et Cryptography pour gérer les
commandes vocales, la synthèse vocale et la cryptographie.
"""

def display(state) :
    if(state["choice_index"] == 3) :
        state["choice_index"] = 0
    elif (state["choice_index"] == -1) :
        state["choice_index"] = 2
    s.set_pixels(state["picks"][state["choice_index"]])


def launch_voice() :
    s.set_pixels(sounds_light()) # animate
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
        events = s.stick.get_events()
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
        s.show_letter(str(count))
    return code


def password_man() :
    f = open("/home/pi/APP3/src/db/password", 'r+')
    code = ""
    numero = ""
    catch_pass = True

    decryptfile = f.readlines()
    if(decryptfile) :
        s.show_message("Code ?")
        s.set_pixels(sounds_light())
        print(decode(decryptfile[0], decryptfile[1]))
        while(True) :
            intent = rhasspy.speech_to_intent()
            if(intent["name"] == "leave") :
                return
            if(intent["name"] == "code" and len(intent["variables"]) == 4) :
                codetotest = ""
                for i in range(4) :
                    codetotest += intent["variables"]["aliments" + str(i)] + ","
                print(decryptfile[0].strip("\n") , "   ", hashing(codetotest))
                if(decryptfile[0].strip("\n") == hashing(codetotest)) :
                    s.show_message("Numero : " + decode(decryptfile[0], decryptfile[1]))
                    break

    while catch_pass:
        f.seek(0)
        events = s.stick.get_events()
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
                        if(decryptfile) :
                            decryptnum = decode(decryptfile[0], decryptfile[1])
                            s.show_message(decryptnum)
                            for c in decryptnum :
                                rhasspy.text_to_speech(c)
                    if(menu["choice_index"] == 1) :
                        numero = launch_voice()
                        catch_pass = False
                    if(menu["choice_index"] == 2) :
                        numero = launch_manual()
                        catch_pass = False
        display(menu)
    s.show_message("Numero : " + numero)
    s.show_message("Dite votre code")


    while True:
        intent = rhasspy.speech_to_intent()
        if(intent["name"] == "code" and len(intent["variables"]) == 4) :
            s.show_message("Code :")
            for i in range(4) :
                code += intent["variables"]["aliments" + str(i)] + ","
                s.show_message(intent["variables"]["aliments" + str(i)])
            break
    
    f.truncate(0)
    print(code)
    f.write(hashing(code) + "\n")
    f.write(encode(hashing(code), numero))




