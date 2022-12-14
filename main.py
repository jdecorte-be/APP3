from src.menu import menu
from sense_hat import SenseHat
import rhasspy as rhasspy


sense = SenseHat()

def main():
    # rhasspy.train_intent_files("sentences.ini")
    menu()

if __name__ == "__main__":
    main()

