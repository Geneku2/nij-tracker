import vt_data_localization.vt_data_scraper as scraper
from vt_data_localization.vt_liver import liver

def main():
    en_list = scraper.get_members(branch="en")
    en_ids = []
    for mem in en_list:
        en_ids.append(scraper.fetch_yt_id(mem))

    en_livers: liver = []
    for id in en_ids:
        temp_liver = liver(id, branch_="en")
        en_livers.append(temp_liver)

    for channel in en_livers:
        channel.write_to_doc()

if __name__ == "__main__":
    main()
