from multiprocessing.spawn import old_main_modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.actions.pointer_actions import PointerActions
import time
import pandas as pd
import pickle
from fuzzywuzzy import process, fuzz

options=Options()
options.headless=False


web='https://m-se.snabbare.com/live-betting/'
PATH="/usr/local/bin/chromedriver"

driver= webdriver.Chrome(PATH, options=options)
driver.get(web)
driver.maximize_window()
time.sleep(2)
#cookie accepter


teams=[]
over_under=[]
odds_events=[]

#gå in på live-fotboll
live=driver.find_element(By.XPATH,'//*[@id="sports-carouselLeft_LiveNowBettingResponsiveBlock_15977"]/sb-comp/div/div/div[3]/div[2]')
if live.text== 'Fotboll':
    live.click()
#dra ned sliders
time.sleep(2)

match_info=driver.find_elements(By.CLASS_NAME, 'rj-ev-list__ev-card__inner')
for info in match_info:
    info_list=list(info.text.split('\n'))
    
    team_names=[]
    odds=[]
    if len(info_list)>=12:
        team_names.append(info_list[-7])
        team_names.append(info_list[-3])
        teams.append(tuple(team_names))
        
        odds.append(info_list[-6])
        odds.append(info_list[-4])
        odds.append(info_list[-2])
        odds_events.append(tuple(odds))
    elif len(info_list)==11:
        team_names.append(info_list[-9])
        team_names.append(info_list[-3])
        teams.append(tuple(team_names))
        
        odds.append(0)
        odds.append(info_list[-4])
        odds.append(info_list[-2])
        odds_events.append(tuple(odds))
    else:
        team_names=['-','-']
        odds=[0.00,0.00,0.00]
        teams.append(tuple(team_names))
        odds_events.append(tuple(odds))

    
    



#scrapea lagnamnen 

#scrapea oddsen


time.sleep(5)
driver.quit()


pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

ScraperDict={'Teams':teams, '1x2':odds_events}

df_snabbare=pd.DataFrame.from_dict(ScraperDict)
df_snabbare=df_snabbare.applymap(lambda x: x.strip() if isinstance(x,str) else x)
output=open('df_snabbare','wb')
pickle.dump(df_snabbare, output)
output.close()
print(df_snabbare)

#denna är riktigt dålig, gör om och snygga till