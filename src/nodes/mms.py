import requests
from flask import Flask, redirect, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import json
import twilio.rest
import asyncio
import random
import datetime


accountsid = "AC9e4a91e0e6865a7d8c5534766f11d532"
authtoken = "05d27a08354de3223e2b9baef869ce43"
client = twilio.rest.Client(accountsid, authtoken)

app = Flask(__name__)
myDict = {"+13017955455": "Rohit"}



i = 0
awaiting_responses = []

@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    global i, awaiting_responses
    r = MessagingResponse()
    try:
        if i == 0:
            os.chdir('../')
            os.chdir('assets')
            i = 1
        else:
            pass
            
        print(request.values['MediaUrl0'])
        print("not 0")
        name = request.values['MessageSid']
        print(os.listdir())
        client.messages.create(body="Great! Who's name do you want this to go under?", from_="+13017195667", to=request.values['From'])
        awaiting_responses.append({request.values['From']: [request.values['MediaUrl0'], datetime.datetime.now()]})
        return "Done"
    except Exception as e:
        for item in awaiting_responses:
            for key, value in item.items():
                print(value)
                if key == request.values['From']:
                    a1 = datetime.datetime.now()
                    a2 = value[1]
                    print(f"a2 = {a2}")
                    if ((a2-a1).total_seconds()) > 60:
                        print("1")
                        awaiting_responses.remove({key: value})
                        return "Hello"
                    else:
                        print("2")
                        personname = request.values['Body'].capitalize()
                        if personname not in os.listdir():
                            os.mkdir(personname)
                        with open((f'{personname}/{random.randint(298301, 1238981273182)}.png'), "wb") as f:
                            f.write(requests.get(value[0]).content)
                    client.messages.create(body="Photo added! Need to add more? Reply with another photo!", from_="+13017195667", to=request.values['From'])
                    awaiting_responses.remove({key: value})

                    

            
        return "Failed"

    return "Good"
if __name__ == "__main__":
    app.run(debug=True)
    print("Yo")
        

