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

            #yuuhi = yuhi
            #Aduchi = Azuchi
            #Uduki = Uzuki
            #Shouichi = Shoichi
            #gundou = gundo



    #    for characterIdx in range(len(names[nameIdx])):
    #        if(names[nameIdx][characterIdx] == '_'):
    #            names[nameIdx] = names[nameIdx][0:characterIdx] + names[nameIdx][characterIdx+1:len(names[nameIdx])]
    #            break

    #for nameIdx in range(len(names)):
    #    numUpper = 0
    #    for characterIdx in range(len(names[nameIdx])):
    #        if(names[nameIdx][characterIdx].isupper()):
    #            numUpper+=1
    #        if numUpper > 1:
    #            names[nameIdx] = names[nameIdx][0:characterIdx] + "-" + names[nameIdx][characterIdx:len(names[nameIdx])]
    #            break
    #    names[nameIdx] = names[nameIdx].lower()
    return names

list = get_members(branch="jp")
list2 = get_members(branch="en")

for item in list:
    print(item)

for item in list2:
    print(item)