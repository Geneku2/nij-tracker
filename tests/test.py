#https://github.com/googleapis/google-api-python-client/blob/main/docs/README.md
from xml.etree.ElementTree import tostring
from requests import Response
from googleapiclient.discovery import build

#adding outer folder to directory
import sys
sys.path.insert(0, './')
import keys

#forUsername = "Gigguk"                     # Gigguk's Username (only legacy channels have usernames)
#id = "animezone"                           # Gigguk's Creator Tag (tags DO NOT WORK as id NOR username so it is USELESS)
myid = "UC7dF9qfBMXrSlaaFFDvV_Yg"            # Gigguk's channelid (found in the HTML)


youtube = build("youtube", "v3", developerKey=keys.api_key)
snippetRequest = youtube.channels().list(part="snippet", id = myid)
statsRequest = youtube.channels().list(part="statistics", id = myid)

username = snippetRequest.execute()["items"][0]["snippet"]["title"]
subcount = statsRequest.execute()["items"][0]["statistics"]["subscriberCount"]

print(username)
print(subcount)