import requests, sense_hat

sense = sense_hat.SenseHat()

def send_msg() :
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = 'from=Vonage APIs&text=The Raspberry need help !&to=32468258791&api_key=4e3e591f&api_secret=Nh2neow7xdfmfDsn'

    response = requests.post('https://rest.nexmo.com/sms/json', headers=headers, data=data)
    print(response)
    sense.show_message("Le messages est envoye !")


def sos() :
    info = {
        "count" : 0,
        "balance" : True,
    }

    while(1) :
        orientation = sense.get_orientation_degrees()
        print(orientation["pitch"])
        if(orientation["pitch"] > 40 and  100 > orientation["pitch"] and info["balance"] == True) :
            info["count"] = info["count"] + 1
            info["balance"] = False
        if(orientation["pitch"] < 40) :
            info["balance"] = True
        if(info["count"] > 3) :
            for i in range(3, 0, -1) :
                sense.show_message(str(i))
            send_msg()
            break

    
