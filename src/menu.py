from src.utils.colors import R,W,O,Y,N,G,O,S,B
from src.sos import sos
from src.password import password_man
from src.courses import courses
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
        
    sense = sense_hat.SenseHat()
    sense.low_light = True

    game_state = { 
            "picks" : (list_de_course(), SOS_menu(), password()),
            "choice_index" : 0,
            }

    def display(state) :
        if(state["choice_index"] == 3) :
            state["choice_index"] = 0
        elif (state["choice_index"] == -1) :
            state["choice_index"] = 2
        sense.set_pixels(state["picks"][state["choice_index"]])
    
    sense.clear()

    ####
    # Main Loop
    ####

    while True:
        events = sense.stick.get_events()
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
        display(game_state)
