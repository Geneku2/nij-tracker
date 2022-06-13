import string
from unicodedata import name
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_members(branch = "en"):

    #Depending on what branch is requested, url is set to said branch
    url = "https://www.nijisanji.jp"
    if (branch == "en"):
        url = "https://www.nijisanji.jp/en/members?order=debut_at"
    elif (branch == "jp"):
        url = "https://www.nijisanji.jp/en/members?filter=%E3%81%AB%E3%81%98%E3%81%95%E3%82%93%E3%81%98&order=debut_at"
    else:
        raise Exception("Given Branch \"" + branch + "\" Is Not Supported")

    #HTML is pulled from respective website
    this_session = HTMLSession()
    request = this_session.get(url)
    request.html.render()

    #HTML is parsed for images with specific tags
    soup = BeautifulSoup(request.html.raw_html, "html.parser")
    div_containers = soup.findAll("img", attrs={"class":"u3qrsl-0 bTAYwC"})     #tags are prone to breaking, may need updates

    #string processing to tidy up list of names
    names = []
    for item in div_containers:
        names.append(str(item["src"]))

    for imageIdx in range(len(names)):
        for characterIdx in range(len(names[imageIdx])-1, -1, -1):
            if(names[imageIdx][characterIdx] == '/'):
                #offset to specifically get the name, may need changes is riku updates website
                names[imageIdx] = names[imageIdx][characterIdx+15:len(names[imageIdx])-10]
                break

    #removes extra characters from name
    for nameIdx in range(len(names)):
        #if follows FirstLast format
        if names[nameIdx].isalnum():
            numUpper = 0
            for characterIdx in range(len(names[nameIdx])):
                if(names[nameIdx][characterIdx].isupper()):
                    numUpper+=1
                if numUpper > 1:
                    names[nameIdx] = names[nameIdx][0:characterIdx] + "-" + names[nameIdx][characterIdx:len(names[nameIdx])]
                    break
        else:
            while names[nameIdx].find("_") != -1:
                names[nameIdx] = names[nameIdx][:names[nameIdx].index("_")] + "-" + names[nameIdx][names[nameIdx].index("_")+1:]
            while names[nameIdx].find("%20") != -1:
                names[nameIdx] = names[nameIdx][:names[nameIdx].index("%20")] + "-" + names[nameIdx][names[nameIdx].index("%20")+3:]
        names[nameIdx] = names[nameIdx].lower()

        #nijisanji, please fix your naming, pleaseee
        if names[nameIdx] == "riri-yuuhi":
            #yuuhi = yuhi
            names[nameIdx] = "riri-yuhi"
        elif names[nameIdx] == "yoko-akabane":
            #yoko = youko
            names[nameIdx] = "youko-akabane"
        elif names[nameIdx] == "momo-aduchi":
            #aduchi = azuchi
            names[nameIdx] = "momo-azuchi"
        elif names[nameIdx] == "kou-uduki":
            #uduki = uzuki
            names[nameIdx] = "kou-uzuki"
        elif names[nameIdx] == "ririmu-makaino":
            #rirmu makaino = makaino ririmu
            names[nameIdx] = "makaino-ririmu"
        elif names[nameIdx] == "shouichi-kanda":
            #shouichi = shoichi
            names[nameIdx] = "shoichi-kanda"
        elif names[nameIdx] == "mirei-gundou":
            #gundou = gundo
            names[nameIdx] = "mirei-gundo"
        elif names[nameIdx] == "suha-min":
            #suha min = min suha
            names[nameIdx] = "min-suha"        
        elif names[nameIdx] == "nagi-so":
            #nagi so = so nagi
            names[nameIdx] = "so-nagi"    
        elif names[nameIdx] == "roha-lee":
            #roha lee = lee roha
            names[nameIdx] = "lee-roha"       
        elif names[nameIdx] == "ray-akira":
            #ray akira = akira ray
            names[nameIdx] = "akira-ray"     
        elif names[nameIdx] == "jiyu-oh":
            #jiyu oh = oh jiyu
            names[nameIdx] = "oh-jiyu"     
        elif names[nameIdx] == "nari-yang":
            #nari yang = yang nari
            names[nameIdx] = "yang-nari"
        elif names[nameIdx] == "hari-ryu":
            #hari ryu = ryu hari
            names[nameIdx] = "ryu-hari"         
          
    return names

def fetch_yt_id(livername):
    #in case wrong format, should take liver name as parsed string
    if not isinstance(livername, str):
        raise Exception(str(livername) + " Is Not a Valid Liver Name")

    #convert to nijisanji page url
    url = "https://www.nijisanji.jp/en/members/" + livername


    #beautiful soup shit
    this_session = HTMLSession()
    request = this_session.get(url)
    request.html.render()

    soup = BeautifulSoup(request.html.raw_html, "html.parser")
    div_containers = soup.findAll("a", attrs={"target":"_blank","rel":"noopener noreferrer"})
    channelID = "none"
    
    #find youtube target reference element
    for item in div_containers:
        if str(item["href"]).find("youtube") != -1:
            channelID = str(item["href"])
            break

    #if liver not found, then channelID is null and throws exception
    if channelID == "none":
        raise Exception("There Is No Liver Named " + livername + " In NIJISANJI")

    #more string parsing to isolate channel ID for YTv3API
    qMarkIdx = len(channelID)-1
    for characterIdx in range(len(channelID)-1, -1, -1):
        if channelID[characterIdx] == '?':
            qMarkIdx = characterIdx
        if channelID[characterIdx] == '/':
            channelID = channelID[characterIdx + 1:qMarkIdx]
            break

    return channelID
    

list = get_members(branch="jp")
for mem in list:
    print(fetch_yt_id(mem))

list = get_members(branch="en")
for mem in list:
    print(fetch_yt_id(mem))