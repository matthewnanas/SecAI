import json
import os

import twilio.rest

with open("security.json") as secur:
    security = json.loads(secur.read())
    secur.close()

accountsid = security["accountID"]
authtoken = security["authToken"]
client = twilio.rest.Client(accountsid, authtoken)

cases = [
    "https://handler.twilio.com/twiml/EHcc17118fc21ef15b711bf26d5329777b", # "Hello, test case."
    "https://handler.twilio.com/twiml/EH37749524b98862ba08a75c2370b1a9f9", # Armed person case
    "https://handler.twilio.com/twiml/EHa9ac8807f1c3f122d959e5b521de2414", # Unknown person case
    "https://handler.twilio.com/twiml/EH034b64c120e69bfcd544f0c572c9d359", # Package delivery case
]

numbers = None

def refreshNumbers():
    global numbers
    os.chdir('../')
    with open('assets/numbers.json') as f:
        numbers = json.load(f)
        numbers = numbers['Numbers']
    os.chdir("./nodes")


def sendMsg(msg):
    refreshNumbers()
    global numbers
    try:
        for number in numbers:
            client.messages.create(body=msg, from_="+13017195667", to=number)
    except Exception as e:
        print(e)
        pass


def makeCall(num):
    if num not in range(0, 3):
        return
    refreshNumbers()
    global numbers
    try:
        for number in numbers:
            client.calls.create(to=number, from_="+13017195667", url=cases[num])
    except Exception as e:
        print(e)
        pass


for i in range(5):
    client.messages.create(body="SecAI Alert: Threat Detected", from_="+13017195667", to="2407014334")
