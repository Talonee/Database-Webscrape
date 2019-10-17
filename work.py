from bs4 import BeautifulSoup as bs # webscrape
import requests # websites
import codecs # files
# import pandas as pd # excel sheets

# request website
# page = requests.get("http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid=83813&cite_number=1306-25673")

def init_excel():
    sheet = {
        "Cite ID": [],
        "Cite Number": [],
        "Date Issued": [],
        "License Number": [],
        "Registered Owner": [],
        "Status": [],
        "Violation": [],
        "Amount": [],
        "State": []
        }
    
    return sheet

def export_excel(table, name):
    df = pd.DataFrame.from_dict(table, orient="index").transpose()
    export_csv = df.to_csv(name, index=False)

def entry_data_mod():
    f = codecs.open("citemgr_2013_small.html", "r", "utf-8")
    soup = bs(f.read(), "html.parser")
    
    sheet = init_excel()
    column = 0

    for i in soup.find_all("td", class_="tblkeypcs"): # Cite ID
        sheet["Cite ID"].append(i.a.get_text())

    for i in soup.find_all("td", class_="tblpcs"): # cite#, date, license, owner, status
        if column == 6:
            column = 0

        if column == 0:
            sheet["Cite Number"].append(i.get_text())
        elif column == 1:
            sheet["Date Issued"].append(i.get_text())
        elif column == 2:
            sheet["License Number"].append(i.get_text())
        elif column == 3:
            sheet["Registered Owner"].append(i.get_text())
        elif column == 4:
            pass
        elif column == 5:
            sheet["Status"].append(i.get_text())

        column += 1
    
    for i in sheet["Cite ID"]:
        url = "http://citemgr/citemgr/cite_edit.php?cite_sysid={}&username=".format(i)
        page = requests.get(url)
        soup2 = bs(page.content, "html.parser")

        state = soup2.find_all("input")
        for i in state:
            if i.get("name") == "license_state":
                sheet["State"].append(i.get("value"))


    #---------------------------------------------------------
    # f2 = codecs.open("citemgr_ex1_transaction.html")
    # soup2 = bs(f2.read(), "html.parser")

    # violation = []
    # viol_number = soup2.find("td", class_="tblpcs").get_text().split()[0]
    # violation.append(viol_number)
    # data.append(violation)

    # for i in sheet:
    #     print("{}: {}".format(i, len(sheet[i])))

    return sheet


if __name__ == "__main__":
    # export_excel(entry_data_mod(), "data_mult.csv")
    print(entry_data_mod())
    # entry_data_mod()
    