from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_members(branch = "en"):
    url = "https://www.nijisanji.jp"
    if (branch == "en"):
        url = "https://www.nijisanji.jp/en/members?order=debut_at"
    elif (branch == "jp"):
        url = "https://www.nijisanji.jp/en/members?filter=%E3%81%AB%E3%81%98%E3%81%95%E3%82%93%E3%81%98&order=debut_at"
    else:
        raise Exception("Given Branch \"" + branch + "\" Is Not Supported")

    this_session = HTMLSession()
    request = this_session.get(url)
    request.html.render()
    soup = BeautifulSoup(request.html.raw_html, "html.parser")
    div_containers = soup.findAll("div", attrs={"class":"bt1fbu-0 fagwEa"})

    names = []
    for item in div_containers:
        names.append(item.text.lower())

    if(branch == "jp"):
        #gotta do some fancy processing here to make sure letters are good
        #also note: consider using image instead because images are formatted correctly
        pass

    return names

list = get_members(branch="jp")

for item in list:
    print(item)