#https://github.com/googleapis/google-api-python-client/blob/main/docs/README.md
from xml.etree.ElementTree import tostring
from requests import Response
from googleapiclient.discovery import build

#adding outer folder to directory
import sys
sys.path.insert(0, './')
import keys


youtube = build("youtube", "v3", developerKey=keys.api_key)
request = youtube.channels().list(
    part="snippet",
    #id="UCS9uQI-jC3DE0L4IpXyvr6w"              #kiryu coco by id
    #forUsername = 'Coco Ch. 桐生ココ'           #kiryu coco by username
    #forUsername = "3y0iPFR93VoEzeFcrB5mcA"     #my dumb ass
    #forUsername = "Gigguk"                     #the biggus giggus
    id = "UC7dF9qfBMXrSlaaFFDvV_Yg"            #the biggus giggus id
    #forUsername = "Niconiconii"                         #ed dan DOESN'T WORK
    #id = "UCH-NXU_A3HmisP1cM1rkm6Q"            #ed dan id

)

response = request.execute()

print(response)
print("\n")
#print(response["items"][0]["snippet"]["title"])