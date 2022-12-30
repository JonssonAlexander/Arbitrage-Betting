import subprocess
import pandas as pd
import pickle 
from fuzzywuzzy import process, fuzz
from sympy import symbols, Eq, solve


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


subprocess.run("python3 scraping_888.py & python3 scraping_snabbare.py & python3 test_unibet.py & wait", shell=True) #antingen detta eller test_unibet.py

df_unibet=pickle.load(open('df_unibet','rb'))
df_unibet=df_unibet[['Teams', '1x2']]

#hur gör man replace med pickle databas 

df_snabbare=pickle.load(open('df_snabbare','rb'))
df_snabbare=df_snabbare[['Teams', '1x2']]

df_888=pickle.load(open('df_888','rb'))
df_888=df_888[['Teams', '1x2']]

teams_1 = df_unibet['Teams'].tolist()
teams_2 = df_snabbare['Teams'].tolist()
teams_3 = df_888['Teams'].tolist()




#automatisera detta för att använda fler spelmäklare
df_unibet[['Teams_matched_unibet_snabbare','Score_unibet_snabbare']] = df_unibet['Teams'].apply(lambda x:process.extractOne(str(x), teams_2, scorer=fuzz.token_set_ratio)).apply(pd.Series) #bytte x till str(x) 
df_unibet[['Teams_matched_unibet_888', 'Score_unibet_888']]=df_unibet['Teams'].apply(lambda x: process.extractOne(str(x), teams_3,scorer=fuzz.token_set_ratio)).apply(pd.Series)
df_888[['Teams_matched_unibet_888', 'Score_unibet_888']] = df_888['Teams'].apply(lambda x:process.extractOne(str(x), teams_1, scorer=fuzz.token_set_ratio)).apply(pd.Series)
df_888[['Teams_matched_snabbare_888', 'Score_snabbare_888']] = df_888['Teams'].apply(lambda x:process.extractOne(str(x), teams_2, scorer=fuzz.token_set_ratio)).apply(pd.Series)
df_snabbare[['Teams_matched_unibet_snabbare', 'Score_unibet_snabbare']] = df_snabbare['Teams'].apply(lambda x:process.extractOne(str(x), teams_1, scorer=fuzz.token_set_ratio)).apply(pd.Series)
df_snabbare[['Teams_matched_snabbare_888', 'Score_snabbare_888']] = df_snabbare['Teams'].apply(lambda x:process.extractOne(str(x), teams_3, scorer=fuzz.token_set_ratio)).apply(pd.Series)


df_surebet_snabbare_888 = pd.merge(df_snabbare, df_888, left_on='Teams_matched_snabbare_888', right_on='Teams')
df_surebet_unibet_888 = pd.merge(df_unibet, df_888, left_on='Teams_matched_unibet_888', right_on='Teams')
df_surebet_unibet_snabbare = pd.merge(df_unibet, df_snabbare, left_on='Teams_matched_unibet_snabbare', right_on='Teams')


df_surebet_snabbare_888=df_surebet_snabbare_888[df_surebet_snabbare_888['Score_snabbare_888_x']>60]
df_surebet_snabbare_888 = df_surebet_snabbare_888[['Teams_x', '1x2_x', 'Teams_y', '1x2_y']]

df_surebet_unibet_888=df_surebet_unibet_888[df_surebet_unibet_888['Score_unibet_888_x']>60]
df_surebet_unibet_888 = df_surebet_unibet_888[['Teams_x', '1x2_x', 'Teams_y', '1x2_y']]

df_surebet_unibet_snabbare=df_surebet_unibet_snabbare[df_surebet_unibet_snabbare['Score_unibet_snabbare_x']>60]
df_surebet_unibet_snabbare = df_surebet_unibet_snabbare[['Teams_x', '1x2_x', 'Teams_y', '1x2_y']]



df_surebet_unibet_snabbare[['1x2_x_1', '1x2_x_2','1x2_x_3']]=pd.DataFrame(df_surebet_unibet_snabbare['1x2_x'].tolist(), index=df_surebet_unibet_snabbare.index).apply(pd.Series).astype(float)
df_surebet_unibet_snabbare[['1x2_y_1', '1x2_y_2','1x2_y_3']]=pd.DataFrame(df_surebet_unibet_snabbare['1x2_y'].tolist(), index=df_surebet_unibet_snabbare.index).apply(pd.Series).astype(float)

df_surebet_unibet_888[['1x2_x_1', '1x2_x_2','1x2_x_3']]=pd.DataFrame(df_surebet_unibet_888['1x2_x'].tolist(), index=df_surebet_unibet_888.index).apply(pd.Series).astype(float)
df_surebet_unibet_888[['1x2_y_1', '1x2_y_2','1x2_y_3']]=pd.DataFrame(df_surebet_unibet_888['1x2_y'].tolist(), index=df_surebet_unibet_888.index).apply(pd.Series).astype(float)

df_surebet_snabbare_888[['1x2_x_1', '1x2_x_2','1x2_x_3']]=pd.DataFrame(df_surebet_snabbare_888['1x2_x'].tolist(), index=df_surebet_snabbare_888.index).apply(pd.Series).astype(float)
df_surebet_snabbare_888[['1x2_y_1', '1x2_y_2','1x2_y_3']]=pd.DataFrame(df_surebet_snabbare_888['1x2_y'].tolist(), index=df_surebet_snabbare_888.index).apply(pd.Series).astype(float)



def find_surebet(frame):
    frame['find_sure_1x2_y_3']= (1/ frame['1x2_x_1'])+(1/ frame['1x2_x_2'])+ 1/ frame['1x2_y_3']
    frame['find_sure_1x2_y_2']= (1/ frame['1x2_x_3'])+(1/ frame['1x2_x_1'])+ 1/ frame['1x2_y_2']
    frame['find_sure_1x2_y_1']= (1/ frame['1x2_x_2'])+(1/ frame['1x2_x_3'])+ 1/ frame['1x2_y_1']
 
    frame['find_sure_1x2_x_3']= (1/ frame['1x2_y_1'])+(1/ frame['1x2_y_2'])+ 1/ frame['1x2_x_3']
    frame['find_sure_1x2_x_2']= (1/ frame['1x2_y_3'])+(1/ frame['1x2_y_1'])+ 1/ frame['1x2_x_2']
    frame['find_sure_1x2_x_1']= (1/ frame['1x2_y_2'])+(1/ frame['1x2_y_3'])+ 1/ frame['1x2_x_1']
    frame=frame[['Teams_x', '1x2_x', 'Teams_y', '1x2_y', 'find_sure_1x2_y_1', 'find_sure_1x2_y_2', 'find_sure_1x2_y_3', 'find_sure_1x2_x_1', 'find_sure_1x2_x_2', 'find_sure_1x2_x_3']]
    frame= frame[(frame['find_sure_1x2_y_1']<1) | (frame['find_sure_1x2_y_2']<1) | (frame['find_sure_1x2_y_3']<1) | (frame['find_sure_1x2_x_1']<1) | (frame['find_sure_1x2_x_2']<1) | (frame['find_sure_1x2_x_3']<1)]
    frame.reset_index(drop=True, inplace=True)
    return frame

df_surebet_snabbare_888=find_surebet(df_surebet_snabbare_888)
df_surebet_unibet_888=find_surebet(df_surebet_unibet_888)
df_surebet_unibet_snabbare=find_surebet(df_surebet_unibet_snabbare)



dict_surebet={'Unibet-Snabbare':df_surebet_unibet_snabbare, 'Snabbare-888':df_surebet_snabbare_888, '888-Unibet':df_surebet_unibet_888}
print(dict_surebet)

def beat_brokers(odds1,odds2,odds3,tot_stake):
    x,y,z=symbols('x y z')
    eq1=Eq(x+y+z-tot_stake, 0)
    eq2=Eq(odds1*y -odds2*x- odds3*z,0)
    stakes=solve((eq1,eq2), (x,y,z))
    tot_investment=stakes[x]+stakes[y]+stakes[z]
    profit1=odds1*stakes[x] -tot_stake
    profit2=odds2*stakes[y] -tot_stake
    profit3=odds3*stakes[z] -tot_stake
    benefit1=f'{profit1/tot_investment*100:.2f}'
    benefit2=f'{profit2/tot_investment*100:.2f}'
    benefit3=f'{profit3/tot_investment*100:.2f}'
    dict_profit={'Odds1':odds1,'Odds2':odds2,'Odds3':odds3,'Stakes1':f'${stakes[x]:.0f}', 'Stakes2':f'${stakes[y]:.0f}', 'Stakes3':f'${stakes[z]:.0f}', 
        'Profit1':f'${profit1:.2f}','Profit2':f'${profit2:.2f}','Profit3':f'${profit3:.2f}','Benefit1':benefit1,'Benefit2':benefit2,'Benefit3':benefit3}
    return dict_profit

tot_stake=100


for x in dict_surebet.keys:
    if x.empty==False:
        ...
#nu är det dags att göra så att den skickar ett mail om den hittar 
























