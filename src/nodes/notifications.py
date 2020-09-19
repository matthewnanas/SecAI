import json
import os

import twilio.rest

accountsid = "AC9e4a91e0e6865a7d8c5534766f11d532"
authtoken = "05d27a08354de3223e2b9baef869ce43"
client = twilio.rest.Client(accountsid, authtoken)

cases = [
    "https://handler.twilio.com/twiml/EHcc17118fc21ef15b711bf26d5329777b", # "Hello, test case."
    "https://handler.twilio.com/twiml/EH37749524b98862ba08a75c2370b1a9f9", # Armed person case
    "https://handler.twilio.com/twiml/EHa9ac8807f1c3f122d959e5b521de2414", # Unknown person case
    "https://handler.twilio.com/twiml/EH034b64c120e69bfcd544f0c572c9d359", # Package delivery case
    ""
    
]

os.chdir('../')
with open('assets/numbers.json') as f:
    numbers = json.load(f)
    numbers = numbers['Numbers']
os.chdir("./nodes")


def sendMsg(msg):
    global numbers
    for number in numbers:
        client.messages.create(body=msg, from_="+13017195667", to=number)


def makeCall(num):
    global numbers
    for number in numbers:
        client.calls.create(to=number, from_="+13017195667", url=cases[num])
