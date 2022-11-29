import sense_hat, random, time


sense = sense_hat.SenseHat()

game_state = { 
          "comp_pick" : None,
          "user_pick" : None,
          "picks" : ("Course", "Tetris", "SOS"),
          "choice_index" : 0,
          "comp_score" : 0,
          "user_score" : 0
        }





def display(state) :
  if(state["choice_index"] == 3) :
    state["choice_index"] = 0
  elif (state["choice_index"] == -1) :
    state["choice_index"] = 2
  sense.show_message(state["picks"][state["choice_index"]])
  


####
# Intro on Program Start
####

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
            display(game_state)
        elif event.direction == 'right':
            game_state["choice_index"] -= 1
            display(game_state)
        # elif event.direction == 'middle':
            # Comp picks randomly
            # game_state["comp_pick"] = random.choice(game_state["picks"])
            # # User picks selected option
            # game_state["user_pick"] = get_user_pick(game_state)
