import requests
import json
import configparser

"""
Librairie d'accès d'utilisation de rhasspy (https://rhasspy.readthedocs.io/en/latest/) rendue disponible pour le P3 du cours de LINFO1001.

"""

def text_to_speech(sentence):
    """
        Lis le contenu d'un string et l'exprime oralement via rhasspy

        :param: (str) sentence: le string à exprimer oralement
        :return: True si le speech a été accepté, sinon False.
        """
    response = requests.post('http://localhost:12101/api/text-to-speech', sentence.encode())
    if response.status_code==200:
        return True
    return False


def speech_to_intent():
    """

    Indique à rhasspy qu'une commande orale va être lancée. Il s'ensuit ensuite un signal sonore qui indique que rhasspy écoute. Après ce signal  sonore, une phrase 
    peut être enregistrée par rhasspy. 

        :param:/
        :return: un dictionnaire contenant 4 champs :
        raw_tokens (list of str) : les mots (tokens) que rhasspy a reconnu 
        ( à des fins de débogage, il est possible que ce que ce rhasspy
         reconnait n'équivait pas 
        tout à fait aux tokens d'une commande vocale.)
        tokens (list of str) : les mots de la commande vocale auxquels rhasspy fait référence (le plus proche).
        name: le nom de la commande vocale auquel rhasspy fait référence. 
        variables (dict) : un nouveau dictionnaire 
                    qui comprend autant de champs que de variables déclarés dans la commande vocale initiale. 
                    La valeur associée à chaque champ correspond au son/string reconnu par 
                    rhasspy. 
        Exemple: 
        ###################### sentences.ini #########################
        [Light]
        states = (allumer| éteindre)
        places = (salon | hall | coridor)
        (<states>){state} la lumière dans le   (<places>){place}


        ################## Python code #####################
        r = speech_to_intent()
        
        ################## Requête vocale ######################
        Prononcer : Allumer la lumière dans le hall 
        
        ##################### Values ############################
        r["name"] = "Light"
        r["tokens"] = ["Allumer", "la" , "lumière", "dans", "le", "hall"]
        r["variables"] = {"state"="allumer", "place" = "hall"}

        
        """
    r = requests.post('http://localhost:12101/api/listen-for-command')
    json_resp = r.json()
    print(json_resp)
    dictionary = {}
    dictionary["raw_tokens"], dictionary["tokens"], dictionary["name"], dictionary["variables"] = list(map(str,json_resp["raw_tokens"])) ,list(map(str,json_resp["tokens"])), str(json_resp["intent"]["name"]), json_resp['slots']
    return  dictionary



def train_intent_files(filename="sentences.ini"):
    """
    Ajoute un nouveau fichier de commandes vocales que rhasspy va apprendre à reconnaitre. Cette commande vocale sera reconnu par son nom (query_name) et sera associé à un certain nombre de phrases (sentences).
    Dans chaque phrase, on peut également ajouter des variables qui seront retournés via la fonction speech_to_intent

    : return: True si le fichier ini était bien formatté et que le training a été réussi
              False si ce n'est pas le cas : mauvais format de fichier ini ou librairie rhasspy non-installée.

    Les phrases ne doivent pas contenir de caractères non verbaux comme les virgules et les points. 
    Les mots facultatifs sont [entre crochets]. 
    Les alternatives sont (séparées | par des | tuyaux).
     Les règles ont un = après leur nom, contiennent éventuellement des {balises}, 
     et sont référencées <par_nom>.


    ############## Format du fichier ini #####################"
    [query_name_1]
    sentences_1 
    sentences_2
    [query_name_2]
    sentences_3
    sentences_4
    [query_name_3]
    variable_1 = ("1"|"2")
    variable_2 = ("3"|"4")
    blabla (<variable_1>){variable_name_1} blalbla (<variable_2>){variable_name_2} blabla
    
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(filename)
    new_query = ""
    for section in config.sections():
        new_query += "\n[{}]".format(section)
        for key in config[section]: 
            new_query += "\n{}".format(key)
    send_response = requests.post('http://localhost:12101/api/sentences',new_query.encode())
    train_response = requests.post("http://localhost:12101/api/train")
    if train_response.status_code == 200 and send_response.status_code == 200: 
        print("Training worked perfectly.")
        return True 
    elif train_response.status_code!=200:
        print("Training could not work.")
        return False
    elif  send_response.status_code != 200:
        print("Sending the .ini file could not work.")
        return False