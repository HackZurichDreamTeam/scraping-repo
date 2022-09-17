import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time

#!pip install webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller

import requests # 2
import json # 3

from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    #"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options = chrome_options)



ggeocode = 'AIzaSyACn8ZsmhM9DjpK6MYUApfscEnQypC6LjY'

#location from google
def get_location_coordinates(location): # 4
    # pass for now
    # Define the base url
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={ggeocode}" # 6
    response = requests.get(geo_url) # 7
    content = response.content.decode("utf8") # 8
    geo_js = json.loads(content) # 9
    geo_status = geo_js["status"] # 10

    if geo_status == "OK": # 11
        geo_elements = geo_js["results"][0] # 12
        geometry = geo_elements["geometry"] # 13
        location_coordinates = geometry["location"] # 14
        location_lat = location_coordinates["lat"] # 15
        location_long = location_coordinates["lng"] # 16
        return (location_lat,location_long)
    else:
        return (None,None)


#get driver start
def scrapeWeather(jsonify=False):
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://severeweather.wmo.int/v2/list.html") #This is a dummy website URL
    try:
        elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "dataTables_scrollBody")) #This is a dummy element
    )
    finally:
        print('loaded')

        #comment this for now..
        #driver.find_element_by_xpath("//select/option[@value='60']").click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    """Scraper getting each row"""
    all = soup.findAll("tbody")[2]
    row = all.findAll('tr')

    rest_info = []

    for i in row:
        infos_row = i.findAll('td')
        for index,j in enumerate(infos_row):
            info = None
            if index == 0:
                info = j.find('span')
                event = info.text

            if index == 4:
                info = j.find('span')
                areas = info.text

            if index == 1:
                #issued time
                issued_time = j.text
            if index == 3:
                country = j.text

            if index == 5:
                regions = j.text

            if index == 2:
                continue
        #append to list for dataframe
        rest_info.append([event,issued_time,country,areas,regions,datetime.today().strftime('%Y-%m-%d %H:%M')])

    df = pd.DataFrame(rest_info, columns = ['Event_type','Issued_time','Country','Areas','Regions','Date'])
    df['Issued_time'] = df["Issued_time"].apply(lambda x: x.split("#")[0])
    df['coordinates'] = df["Areas"] + ", " + df["Country"]
    df["geo_location"] = df["coordinates"].apply(get_location_coordinates)


    if jsonify:
        result = df.to_json(orient="split")
        parsed = json.loads(result)
        return json.dumps(parsed)
    else:
        df.to_csv("scraped_weather.csv",mode='a', index=False,header=False)#insert header=False
        return


def scrapePirates(jsonify=False):
    URL = "https://www.icc-ccs.org/index.php/piracy-reporting-centre/live-piracy-report"
    rest_info  =[]
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html.parser')
    all = soup.find("tbody")
    row = all.findAll('tr')
    for i in row:
            infos_row = i.findAll('td')
            for index,j in enumerate(infos_row):
                if index == 0:
                    attack_number =  j.text.replace('\n','').replace('\t','').replace('\r','')
                if index == 1:
                    narrations = j.text.replace('\n','').replace('\t','').replace('\r','')
                if index ==2:
                    date_of_incident = j.text.replace('\n','').replace('\t','').replace('\r','')
                if index >2:
                    continue
            try: 
                rest_info.append([attack_number,narrations,date_of_incident,datetime.today().strftime('%Y-%m-%d %H:%M')])
            except:
                continue

    df_pirates = pd.DataFrame(rest_info, columns = ['attack_nr','text','date_of_incident','scrape_date'])
    df_pirates['text'] = df_pirates["text"].apply(lambda x: x.split("Posn: ")[1])
    df_pirates['location'] = df_pirates["text"].apply(lambda x: x.split(",")[1].split(".")[0] if ":" in x.split(",")[0] else x.split(".")[0])
    df_pirates["geo_location"] = df_pirates["location"].apply(get_location_coordinates)

    if jsonify:
        result = df_pirates.to_json(orient="split")
        parsed = json.loads(result)
        return json.dumps(parsed)
    else:
        df_pirates.to_csv("scraped_pirates.csv",mode='a', index=False,header=False)
        return
    
scrapeWeather()
scrapePirates()
