import datetime
from unicodedata import name
from googleapiclient.discovery import build

import sys
sys.path.insert(0, './')
import keys

#Mashiro liverid="UCfki3lMEF6SGBFiFfo9kvUA"

class liver:

    #constructor required id to target liver, branch is optional
    def __init__(self, id_, branch_ = None):
        if id_ == 0:
            return

        self.id = id_

        youtube = build("youtube", "v3", developerKey=keys.api_key)
        snippetRequest = youtube.channels().list(part="snippet", id = id_).execute()
        statsRequest = youtube.channels().list(part="statistics", id = id_).execute()

        if ("items" not in snippetRequest or "items" not in statsRequest):
            raise Exception("The ChannelID " + id_ + " Has Been Suspended, Terminated Or Doesn't Exist")

        self.name = snippetRequest["items"][0]["snippet"]["title"]
        self.subcount = statsRequest["items"][0]["statistics"]["subscriberCount"]
        self.last_date = datetime.date.today().strftime("%m/%d/%Y")
        self.branch = branch_

    def write_to_doc(self, doc, branch = None):
        pass

    def getCSV(self):
        return self.id + ", " + self.name + ", " + self.last_date + ", " + self.subcount

    def setBranch(self,newBranch: str):
        self.branch = newBranch

#idk is line below is valid not tested
p = liver("UCckdfYDGrjojJM28n5SHYrA")
print(p.getCSV())