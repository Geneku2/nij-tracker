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
    #forUsername = "Gigguk"                     # Gigguk's Username (only legacy channels have usernames)
    #id = "animezone"                           # Gigguk's Creator Tag (tags DO NOT WORK as id NOR username so it is USELESS)
    id = "UC7dF9qfBMXrSlaaFFDvV_Yg"            # Gigguk's channelid (found in the HTML)

)

response = request.execute()

print(response)
print()
print(response["items"][0]["snippet"]["title"])