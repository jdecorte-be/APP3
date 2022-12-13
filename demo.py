import rhasspy
from sense_hat import SenseHat

sense = SenseHat()

# Lance l'apprentissage du fichier sentences.ini. Commentez cette partie si vous souhaitez ne pas le lancer 
sense.show_letter("A")
print("Lancement de l'apprentissage.")
rhasspy.train_intent_files("/home/pi/sentences.ini")
print("Apprentissage terminé.")

x = True

while x:
    sense.show_letter("?")
    # Introduction énoncée
    rhasspy.text_to_speech("Énoncez votre phrase, s'il vous plait.")

    # Réception d'une commande vocale et affichage du résultat.
    intent = rhasspy.speech_to_intent()
    print(intent)

    # Enonce la commande vocale reçue et les variables.
    rhasspy.text_to_speech("Vous avez lancé la commande {} avec les paramètres {}".format(intent["name"], intent["variables"]))

    # Affiche la commande vocale reçue.
    sense.show_message("Commande : {}".format(intent["name"]), scroll_speed=0.07)
    if intent == "GetTemperature":
        hum = sense.get_temperature()
        sense.show_message(hum)
    elif intent == "Exit":
        x = False