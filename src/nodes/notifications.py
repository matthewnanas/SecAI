import twilio.rest

accountsid = "AC9e4a91e0e6865a7d8c5534766f11d532"
authtoken = "05d27a08354de3223e2b9baef869ce43"
client = twilio.rest.Client(accountsid, authtoken)


def sendMsg(msg, numbers):
    for x in numbers:
        client.messages.create(body=msg, from_="+13017195667", to=x)
