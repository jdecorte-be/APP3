import requests, sense_hat

sense = sense_hat.SenseHat()

def send_msg() :
    headers = {
        'Authorization': 'Bearer fd1f12ec77ca4788a1b5b9185941b3de',
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'from': '447520651702',
        'to': [
            '32468258791',
        ],
        'body': 'The Raspberry need help !',
    }

    response = requests.post('https://sms.api.sinch.com/xms/v1/d05fb5eb096d49da8f5173dbdf62e5fd/batches', headers=headers, json=json_data)

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    data = '\n  {\n    "from": "447520651702",\n    "to": [ "32468258791" ],\n    "body": "Enter test message here"\n  }'
    response = requests.post('https://sms.api.sinch.com/xms/v1/d05fb5eb096d49da8f5173dbdf62e5fd/batches', headers=headers, data=data)
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
            for i in range(4) :
                sense.show_message(str(i))
            send_msg()
            break

    
