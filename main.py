from src.menu import menu
from sense_hat import SenseHat
import rhasspy as rhasspy


sense = SenseHat()

def main():
    # print("Lancement de l'apprentissage.")
    # rhasspy.train_intent_files("sentences.ini")
    # print("Apprentissage terminé.")
    # while True :
    #     intent = rhasspy.speech_to_intent()
    #     print(intent["name"])
    #     if(intent["name"] == "Unlock") :
    #         break
    menu()

if __name__ == "__main__":
    main()

