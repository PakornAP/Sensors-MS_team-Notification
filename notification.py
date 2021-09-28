import pymsteams
from get_value_yaml import get_value

def send_text(line1,line2,line3,line4,mode):
    # You must create the connectorcard object with the Microsoft Webhook URL
    Webhooks_URL = get_value('Webhooks_URL')
    myTeamsMessage = pymsteams.connectorcard(Webhooks_URL)
    # Add title
    myTeamsMessage.title(mode)
    # Add text to the message.
    myTeamsMessage.text(line1+'   \n'+line2+'   \n'+line3+'   \n'+line4)
    # send the message.
    myTeamsMessage.send()


