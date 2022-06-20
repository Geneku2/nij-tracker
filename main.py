from genericpath import exists
import vt_data_localization.vt_data_scraper as scraper
from vt_data_localization.vt_liver import liver
from datetime import date

def main():

    #If the document exists, check is each branch has been logged today
    if exists("vt_data_localization/last_update.txt"):
        log = open("vt_data_localization/last_update.txt", "r")
        lines = log.read().split("\n")
        log.close()
        en_check = False
        jp_check = False
        for line in lines:
            status = line.split(" ")
            if status[0] == "jp" and status[1] == date.today().strftime("%m/%d/%Y"):
                jp_check = True
            elif status[0] == "en" and status[1] == date.today().strftime("%m/%d/%Y"):
                en_check = True

        #updates each respective document for the un-updated branches
        if not jp_check:
            update_branch_csv("jp")
            log = open("vt_data_localization/last_update.txt", "w")
            log.write("jp " + date.today().strftime("%m/%d/%Y") + "\n" + lines[1])
            log.close()
        if not en_check:
            update_branch_csv("en")
            log = open("vt_data_localization/last_update.txt", "w")
            log.write(lines[0] + "\nen " + date.today().strftime("%m/%d/%Y"))
            log.close()

    #otherwise, create the document and log livers
    else:
        log = open("vt_data_localization/last_update.txt", "w")
        log.write("jp " + date.today().strftime("%m/%d/%Y") + "\nen " + date.today().strftime("%m/%d/%Y"))
        log.close()

        branches_list = ["en","jp"]
        for item in branches_list:
            update_branch_csv(item)


def update_branch_csv(lang: str):

    id_list = []

    #if there already exists a list of ids
    if exists("vt_data_localization/" + lang + "_ids.txt"):
        file = open("vt_data_localization/" + lang + "_ids.txt", "r")
        id_list = file.read().split("\n")
        file.close()

    #list of the parsed names of livers the the lang branch
    name_list = scraper.get_members(branch_=lang)

    #if there are a different number of livers (either added or removed) we update the id list
    if len(id_list)-1 != len(name_list):
        id_list.clear()
        #converts the list of parsed names into YT channel id by going to the NIJISANJI website
        for mem in name_list:
            id_list.append(scraper.fetch_yt_id(mem))
        
        file = open("vt_data_localization/" + lang + "_ids.txt", "w")
        for id in id_list:
            file.write(id + "\n")
        file.close()
    
    #now, either a file with ids exists or has been created, we read the ids from the file to generate liver objs via YTv3API
    file = open("vt_data_localization/" + lang + "_ids.txt", "r")
    id_list = file.read().split("\n")
    file.close()

    liver_list: liver = []
    for id in id_list[:-1]:
        try:
            temp_liver = liver(id, branch_=lang)
            liver_list.append(temp_liver)
        except:
            print("A Liver Has A Unreadable Channel - Likely Mashiro")

    #writes the liver's information to the appropriate document
    for channel in liver_list:
        channel.write_to_doc()

if __name__ == "__main__":
    main()
