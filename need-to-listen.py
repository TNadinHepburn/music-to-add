# def getKPROFILES():
#     page = requests.get(urlKPROFILES)
#     soup = BeautifulSoup(page.text, 'lxml')
# getKPROFILES()
# urlKPROFILES = f"https://kprofiles.com/{month}-{year}-comebacks-debuts-releases/"

#Import Libraries
from datetime import datetime
from bs4 import BeautifulSoup
import requests, pandas as pd, numpy as  np

def getDBKPOP():
    try:
        page = requests.get(urlDBKPOP)
        print(page)
        soup = BeautifulSoup(page.text, 'lxml')
        table1 = soup.find('table', id='table_1')
        headers = []
        for i in table1.find_all('th'):
            title = i.text
            headers.append(title)
        mydata = pd.DataFrame(columns = headers)
        for j in table1.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(mydata)
            mydata.loc[length] = row
        mydata.drop(['Release', 'Song Title', 'Album Type', 'Artist Type'], axis=1, inplace=True)
        mydata.columns.values[2] = 'Album'
        return mydata
    except:
        print(f'Failed to fetch {year} {month} from DB KPOP')
        return pd.DataFrame(columns = ['Date','Artist','Album'])

def getKPOPOFFICIAL():
    try:
        if (year < 2020 or (year == 2020 and months.index(month) < 5)):
            # Before site strarted
            raise Exception
        elif ((year == 2020 and months.index(month) == 11) or (year == 2021 and months.index(month) < 10)):
            # comebacks = nov20 jan21-oct21
            page = requests.get(urlKPOPOFFICIAL_comebacks)
        else:
            # comeback  = may20-oct20 dec20 nov21-present
            page = requests.get(urlKPOPOFFICIAL_comeback)
        print(page)
        soup = BeautifulSoup(page.text, 'lxml')
        mydatalist = soup.find_all('table')
        mydatalist.pop()
        mydatalist.pop(0)
        mydata = pd.DataFrame(columns = ['Date','Artist','Album'])
        for i in range (len(mydatalist)):
            for j in mydatalist[i].find_all('tr')[1:]:
                row_data = j.find_all('td')
                artist = row_data[1].find('mark').text
                # album = row_data[1].text.replace(row_data[2].text,"")
                row = [k.text for k in row_data]
                row.append(row[1].replace(artist,""))
                row[1]=artist
                row[0] = datetime.strptime(row[0],'%B %d, %Y').strftime('%Y-%m-%d')
                length = len(mydata)
                mydata.loc[length] = row
        return mydata
    except:
        print(f'Failed to fetch {year} {month} KPOP Official')
        return pd.DataFrame(columns = ['Date','Artist','Album'])

def getKPOPMAP():
    try:
        page = requests.get(urlKPOPMAP)
        print(page)
        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.find("div", id="comeback-wrap").find('table').find('tbody').find_all('tr')
        tableOfComebacks = []
        latestDate = ''
        for tr in table:
            try:
                if (tr.find('h2') != None):
                    latestDate = datetime.strptime(tr.find('h2').text,'%b %d, %Y').strftime('%Y-%m-%d')
                else:
                    tempAdd = []
                    tempAdd.append(latestDate)
                    tempAdd.append(tr.find('h3',{"class":'artist-name'}).text)
                    tempAdd.append(tr.find('p',{"class":'album-info'}).text)
                    tableOfComebacks.append(tempAdd)
            except:
                next = True
        mydata = pd.DataFrame(columns = ['Date','Artist','Album'])
        for row in tableOfComebacks:
            length = len(mydata)
            mydata.loc[length] = row
        return mydata
    except:
        print(f'Failed to fetch {year} {month} KPOP Map')
        return pd.DataFrame(columns = ['Date','Artist','Album'])

# COMPLETED
# getDBKPOP()
# getKPOPOFFICIAL()
# getKPOPMAP()

months = ['','january','february','march','april','may','june','july','august','september','october','november','december']
years = [2022,2023,2024]
for year in years[:1]:
    for month in months[10:]:
        urlDBKPOP = f"https://dbkpop.com/{month}-{year}-k-pop-comebacks-and-debuts/"
        urlKPOPMAP = f"https://www.kpopmap.com/update-{month}-{year}-k-pop-comeback-debut-schedule-lineup/"
        urlKPROFILES = f"https://kprofiles.com/{month}-{year}-comebacks-debuts-releases/"
        urlKPOPOFFICIAL_comeback = f"https://kpopofficial.com/kpop-comeback-schedule-{month}-{str(year)}/"
        urlKPOPOFFICIAL_comebacks = f"https://kpopofficial.com/kpop-comebacks-schedule-{month}-{str(year)}/"
        # comeback  = may20-oct20 dec20 nov21-present
        # comebacks = nov20 jan21-oct21

        combined = pd.concat([getDBKPOP(), getKPOPOFFICIAL(), getKPOPMAP()],ignore_index=True)
        combined.sort_values(by=['Date','Artist'], inplace=True)
        combined.to_csv(f'comebacks/{year}-{month}.csv',index=False, encoding='UTF-8')

# month = months[8]
# year = 2022

# urlDBKPOP = f"https://dbkpop.com/{month}-{year}-k-pop-comebacks-and-debuts/"
# urlKPOPMAP = f"https://www.kpopmap.com/update-{month}-{year}-k-pop-comeback-debut-schedule-lineup/"
# urlKPOPOFFICIAL_comeback = f"https://kpopofficial.com/kpop-comeback-schedule-{month}-{str(year)}/"
# urlKPOPOFFICIAL_comebacks = f"https://kpopofficial.com/kpop-comebacks-schedule-{month}-{str(year)}/"

# getDBKPOP()
# getKPOPOFFICIAL()
# getKPOPMAP()


