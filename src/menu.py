from src.utils.colors import R,W,O,Y,N,G,O,S,B
from src.sos import sos
from src.password import password_man
from src.courses import courses
from src.tetris import tetris

import sense_hat

def menu() :
    # Menu Frames
    def password():
        logo = [
        N, N, N, N, N, N, N, N, 
        N, N, S, S, S, S, N, N,
        N, N, S, N, N, S, N, N, 
        N, Y, Y, Y, Y, Y, Y, N,
        N, Y, Y, Y, Y, Y, Y, N,
        N, Y, Y, Y, Y, Y, Y, N,
        N, N, Y, Y, Y, Y, N, N,
        N, N, N, N, N, N, N, N,
        ]
        return logo

    def list_de_course():
        logo = [
        W, W, W, W, W, W, W, W,
        W, W, W, O, O, W, W, W,
        W, W, O, W, W, O, W, W,
        W, O, O, O, O, O, O, W,
        W, O, O, O, O, O, O, W,
        W, O, O, O, O, O, O, W,
        W, O, O, O, O, O, O, W,
        W, W, W, W, W, W, W, W,
        ]
        return logo

    def SOS_menu():
        logo = [
        W, W, W, W, W, W, W, W, 
        W, W, W, R, R, W, W, W,
        W, W, W, R, R, W, W, W, 
        W, R, R, R, R, R, R, W,
        W, R, R, R, R, R, R, W,
        W, W, W, R, R, W, W, W,
        W, W, W, R, R, W, W, W,
        W, W, W, W, W, W, W, W,
        ]
        return logo

    def tetris_menu():
        logo = [
        W, W, W, W, W, W, W, W, 
        W, B, B, B, B, W, Y, W,
        W, W, W, W, W, W, Y, W, 
        W, G, G, W, W, W, Y, W,
        W, G, G, W, W, Y, Y, W,
        O, W, W, W, W, W, W, W,
        O, O, W, W, R, R, R, W,
        W, O, W, W, W, R, W, W,
        ]
        return logo
    
    s = sense_hat.SenseHat()
    s.low_light = True

    game_state = { 
            "picks" : (list_de_course(), SOS_menu(), password(), tetris_menu()),
            "choice_index" : 0,
            }

    def display(state) :
        if(state["choice_index"] == 4) :
            state["choice_index"] = 0
        elif (state["choice_index"] == -1) :
            state["choice_index"] = 3
        s.set_pixels(state["picks"][state["choice_index"]])
    
    s.clear()


    """
    Ce code utilise le Sense HAT, une carte d'extension mat??rielle pour le Raspberry Pi,
    pour afficher un menu sur la matrice LED 8x8 du Sense HAT. Le menu comprend trois options :
    une liste de courses, un appel SOS et une option pour g??rer un mot de passe. L'utilisateur
    peut naviguer dans le menu en utilisant le joystick du Sense HAT et s??lectionner une option
    en appuyant sur le joystick.
    
    Chaque option lance une fonction correspondante qui effectue une action sp??cifique.
    Le code utilise ??galement des couleurs pr??d??finies pour afficher
    des motifs de lumi??res sur la matrice LED.
    """
    ####
    # Main Loop
    ####

    while True:
        events = s.stick.get_events()
        if events:
            for event in events:
                if event.action != 'pressed':
                    #this is a hold or keyup; move on
                    continue
                if event.direction == 'left':
                    game_state["choice_index"] += 1
                elif event.direction == 'right':
                    game_state["choice_index"] -= 1
                elif event.direction == 'middle':
                    # User picks selected option
                    if(game_state["choice_index"] == 0) :
                        courses()
                    if(game_state["choice_index"] == 1) :
                        sos()
                    if(game_state["choice_index"] == 2) :
                        password_man()
                    if(game_state["choice_index"] == 3) :
                        tetris()
        display(game_state)
        sleep(0.1)