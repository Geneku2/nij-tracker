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

        #only allows for existing branches
        if(branch_ == "en" or branch_ == "jp"):
            self.branch = branch_
        else:
            self.branch = None

    #gets subcount only from youtube API
    def fetch_subcount(self):
        youtube = build("youtube", "v3", developerKey=keys.api_key)
        statsRequest = youtube.channels().list(part="statistics", id = self.id).execute()

        if ("items" not in statsRequest):
            raise Exception("The ChannelID " + self.id + " Has Been Suspended, Terminated Or Doesn't Exist")

        self.subcount = statsRequest["items"][0]["statistics"]["subscriberCount"]
        self.last_date = datetime.date.today().strftime("%m/%d/%Y")

    def write_to_doc(self, branch_ = "unk"):
        
        #case if liver has existing valid branch
        if(self.branch != None):
            f = open("vt_data_localization/" + self.branch + "_csv.txt", "a", encoding="utf-8")
            f.write(self.getCSV() + "\n")
            f.close()

        #if liver doesn't have a valid branch and argument branch is valid
        elif (branch_ == "en" or branch_ == "jp"):
            self.branch = branch_
            f = open("vt_data_localization/" + branch_ + "_csv.txt", "a", encoding="utf-8")
            f.write(self.getCSV() + "\n")
            f.close()

        #otherwise, it is unknown and is treated as such
        else:
            f = open("vt_data_localization/unk_csv.txt", "a", encoding="utf-8")
            f.write(self.getCSV() + "\n")
            f.close()

    def getCSV(self):
        return self.id + ", " + self.name + ", " + self.last_date + ", " + self.subcount

    def setBranch(self,newBranch: str):
        self.branch = newBranch

#idk is line below is valid not tested
#p = liver("UCckdfYDGrjojJM28n5SHYrA", branch_="Grvesc")
#p.write_to_doc()