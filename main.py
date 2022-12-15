from src.menu import menu
from sense_hat import SenseHat
import rhasspy as rhasspy


s = SenseHat()

def main():
    # rhasspy.train_intent_files("sentences.ini") // si besoin d'entrainement
    menu()

if __name__ == "__main__":
    main()

