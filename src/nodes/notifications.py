import twilio.rest
import os

accountsid = "AC9e4a91e0e6865a7d8c5534766f11d532"
authtoken = "05d27a08354de3223e2b9baef869ce43"
client = twilio.rest.Client(accountsid, authtoken)

os.chdir('../')
with open('assets/numbers.txt', 'r') as f:
    numbers = f.readlines()
os.chdir('./nodes')

def sendMsg(msg):
    global numbers
    for number in numbers:
        client.messages.create(body=msg, from_="+13017195667", to=number.strip('\n'))
