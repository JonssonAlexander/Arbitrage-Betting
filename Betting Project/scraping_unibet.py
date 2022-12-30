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


options=Options()
options.headless=False


web='https://www.unibet.se/betting/sports/filter/football/all/matches'
PATH="/usr/local/bin/chromedriver"

driver= webdriver.Chrome(PATH, options=options)
driver.get(web)
driver.maximize_window()

time.sleep(2)
accept=driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
accept.click()

live= driver.find_element(By.XPATH, '//*[@id="rightPanel"]/div[3]/div/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/div/button[2]')
live.click()

test=False
b=2




time.sleep(2)
for x in range(15):
    try:
        webber='//*[@id="rightPanel"]/div[3]/div/div/div[1]/div/div/div/div[2]/div[1]/div/div[5]/div[{}]/div/div'.format(x)
               
                
        test=driver.find_element(By.XPATH,webber)
        test.click()
        time.sleep(0.01)
    except:
        pass
time.sleep(2)




teams=[]
over_under=[]
odds_events=[]

sports_title=driver.find_element(By.ID, 'main')
parent=sports_title.find_elements(By.CLASS_NAME,'_20e33')
for child in parent:
    team_names=child.find_elements(By.CLASS_NAME, 'c539a')
    
    alist=[]
    for team in team_names:
        
        alist.append(team.text)
        
    teams.append(tuple(alist))
    odds_event=child.find_elements(By.CLASS_NAME, '_3373b')
    blist=[]
    for odds in odds_event:
        blist.append(odds.text)
    if len(blist)>2:
        
        blist.remove(blist[4])
        blist.remove(blist[3]) 
    if len(blist)<=2:
        blist=[0.00,0.00,0.00] 
    if blist[2]=='':
         blist=[0.00,0.00,0.00] 
    odds_events.append(tuple(blist))
time.sleep(2)
driver.quit()
#for odds in odds_events:
 #       if odds[4]:
  #          over_under_list=[]
   #         over_under_list.append(odds[3])
    #        over_under_list.append(odds[4])
     #       odds.remove(odds[4])
      #      odds.remove(odds[3])
       #     over_under.append(over_under_list)
#







pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

ScraperDict={'Teams':teams, '1x2':odds_events}

df_unibet=pd.DataFrame.from_dict(ScraperDict)
df_unibet=df_unibet.applymap(lambda x: x.strip() if isinstance(x,str) else x)
output=open('df_unibet','wb')
pickle.dump(df_unibet, output)
output.close()
print(df_unibet)
