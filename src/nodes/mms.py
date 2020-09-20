import requests
from flask import Flask, redirect, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import json
import twilio.rest
import asyncio
import random
import datetime


with open("security.json") as secur:
    security = json.loads(secur.read())
    secur.close()

accountsid = security["accountID"]
authtoken = security["authToken"]

client = twilio.rest.Client(accountsid, authtoken)

app = Flask(__name__)

i = 0
awaiting_responses = []

@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    global i, awaiting_responses
    r = MessagingResponse()
    try:
        print(request.values['MediaUrl0'])

        if i == 0:
            os.chdir('../')
            os.chdir('assets')
            i = 1
        else:
            pass

        name = request.values['MessageSid']
        client.messages.create(body="Great! Who's name do you want this to go under?", from_="+13017195667", to=request.values['From'])
        awaiting_responses.append({request.values['From']: [request.values['MediaUrl0'], datetime.datetime.now()]})
        return "Done"
    except Exception as e:
        print(e)
        found = False
        for item in awaiting_responses:
            for key, value in item.items():
                if key == request.values['From']:
                    a3 = datetime.datetime.now()-value[1]
                    if a3.total_seconds() > 60:
                        awaiting_responses.remove({key: value})
                        client.messages.create(body="Timed out! Please try again by sending another image.", from_="+13017195667", to=request.values['From'])
                        found = True
                        return "Hello"
                    else:
                        found = True
                        personname = request.values['Body'].capitalize()
                        if personname not in os.listdir():
                            os.mkdir(personname)
                        with open((f'{personname}/{random.randint(298301, 1238981273182)}.png'), "wb") as f:
                            f.write(requests.get(value[0]).content)
                    client.messages.create(body="Photo added! Need to add more? Reply with another photo!", from_="+13017195667", to=request.values['From'])
                    awaiting_responses.remove({key: value})
        if not found:
            client.messages.create(body="Please send an image file!", from_="+13017195667", to=request.values['From'])


                    

            
        return "Failed"

    return "Good"
if __name__ == "__main__":
    app.run(debug=True)