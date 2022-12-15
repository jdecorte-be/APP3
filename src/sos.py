import requests, sense_hat

s = sense_hat.SenseHat()

"""
Ce code utilise le Sense HAT, une carte d'extension matérielle pour le Raspberry Pi,
pour envoyer un SMS d'urgence à un numéro prédéfini lorsque l'utilisateur effectue un
geste spécifique avec le Raspberry Pi. Le geste est détecté en utilisant les capteurs
d'orientation du Sense HAT pour mesurer l'inclinaison du Raspberry Pi. Si l'utilisateur incline le
Raspberry Pi à un angle supérieur à 40 degrés et inférieur à 100 degrés, une compteur est incrémenté.

Si le compteur atteint un certain nombre de fois, un SMS est envoyé en utilisant les API Nexmo. Le code
utilise également le package Requests pour gérer les requêtes HTTP.
"""


def send_msg():
    """
    Cette fonction envoie un SMS à un numéro prédéfini en utilisant les API Nexmo.
    """

    # Définir les en-têtes pour la requête HTTP
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Définir les données pour la requête HTTP
    data = "from=Vonage APIs&text=The Raspberry need help !&to=32468258791&api_key=4e3e591f&api_secret=Nh2neow7xdfmfDsn"

    # Envoyer la requête HTTP en utilisant les API Nexmo
    response = requests.post(
        "https://rest.nexmo.com/sms/json", headers=headers, data=data
    )

    # Afficher un message pour indiquer que le SMS a été envoyé
    s.show_message("Le messages est envoye !")


def sos():
    """
    Cette fonction détecte un geste spécifique en utilisant les capteurs d'orientation du Sense HAT et envoie un SMS d'urgence lorsque le geste est détecté.
    """

    # Initialiser les variables pour la détection du geste
    info = {
        "count": 0,  # Compteur pour le nombre de fois où le geste a été détecté
        "balance": True,  # Booléen pour indiquer si le Raspberry Pi est à l'horizontale
    }

    # Boucle infinie
    while 1:
        orientation = s.get_orientation_degrees()
        print(orientation["pitch"])
        if (
            orientation["pitch"] > 40
            and 100 > orientation["pitch"]
            and info["balance"] == True
        ):
            info["count"] = info["count"] + 1
            info["balance"] = False
        if orientation["pitch"] < 40:
            info["balance"] = True
        if info["count"] > 3:
            for i in range(3, 0, -1):
                s.show_message(str(i))
            send_msg()
            break
