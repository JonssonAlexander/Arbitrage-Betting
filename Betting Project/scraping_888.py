

from gettext import find
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pickle
from fuzzywuzzy import process, fuzz
from sympy import comp


options=Options()
options.headless=False


web='https://www.888sport.se/livejustnu/fotboll/ips-2/'
PATH="/usr/local/bin/chromedriver"

driver= webdriver.Chrome(PATH, options=options)
driver.get(web)
driver.maximize_window()

time.sleep(2)
accept=driver.find_element(By.ID,'onetrust-accept-btn-handler')
accept.click()

teams=[]
over_under=[]
odds_events=[]
range_teams=0

test=driver.find_elements(By.CLASS_NAME,'bb-sport-event')
for info in test:
    alist=[]
    blist=[]
    info_list=list(info.text.split('\n'))
    if info_list[-1]!='AVSTÄNGD' and len(info_list)==8:
        alist.append(info_list[-3])
        alist.append(info_list[-2])
        alist.append(info_list[-1])
        blist.append(info_list[0])
        blist.append(info_list[2])
    elif len(info_list)==7:
        alist.append(0.00)
        alist.append(info_list[-2])
        alist.append(info_list[-1])
        blist.append(info_list[0])
        blist.append(info_list[2])
    else: 
        alist=[0.00,0.00,0.00]
        blist=['-','-']
     
    odds_events.append(tuple(alist))
    teams.append(tuple(blist))
time.sleep(1)
driver.quit()

pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

ScraperDict={'Teams':teams, '1x2':odds_events}

df_888=pd.DataFrame.from_dict(ScraperDict)
df_888=df_888.applymap(lambda x: x.strip() if isinstance(x,str) else x)
output=open('df_888','wb')
pickle.dump(df_888, output)
output.close()
print(df_888)
