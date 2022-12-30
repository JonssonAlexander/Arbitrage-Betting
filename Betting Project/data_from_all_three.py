df_surebet_snabbare_888 = pd.merge(df_snabbare, df_888, left_on='Teams_matched_snabbare_888', right_on='Teams')

for x in df_surebet_unibet_snabbare.columns:
    print(x)
for x in df_surebet_snabbare_888.columns:
    print(x)
df_surebet_unibet_snabbare_888 = pd.merge(df_surebet_unibet_snabbare,df_surebet_snabbare_888,on='Teams_matched_snabbare_888',how='left')

print(df_surebet_unibet_snabbare_888)
for x in df_surebet_unibet_snabbare_888.columns:
    print(x)

df_surebet_unibet_snabbare_888 = df_surebet_unibet_snabbare_888[df_surebet_unibet_snabbare_888['Score_snabbare_888_x']>60]
df_surebet_unibet_snabbare_888 = df_surebet_unibet_snabbare_888[df_surebet_unibet_snabbare_888['Score_snabbare_888_y']>60]
df_surebet_unibet_snabbare_888 = df_surebet_unibet_snabbare_888[df_surebet_unibet_snabbare_888['Score_unibet_snabbare']>60]
print(df_surebet_unibet_snabbare_888)

df_surebet_unibet_snabbare_888 = df_surebet_unibet_snabbare_888[df_surebet_unibet_snabbare_888['Score_unibet_888']>60]
print(df_surebet_unibet_snabbare_888)
for x in df_surebet_unibet_snabbare_888.columns:
    print(x)

df_surebet_unibet_snabbare_888 = df_surebet_unibet_snabbare_888[['Teams_x_x', '1x2_x_x', 'Teams_y_x', '1x2_y_x','Teams_y_y','1x2_y_y']]
print(df_surebet_unibet_snabbare_888)



frame['find_sure_1x2_y_3']= (1/ float (frame['1x2_x_1']))+(1/ float(frame['1x2_x_2']))+ 1/ float(frame['1x2_y_3'])

tot_stake=100
for frame in dict_surebet:
    if len(dict_surebet[frame])>=1:
        print('------------------SUREBETS Found! '+ frame +' (check team names)--------------------------------------------------')
        print(dict_surebet[frame])
        print('------------------Stakes-------------------------')
        for i, value in enumerate(dict_surebet[frame]['sure_btts1']):
            if value<1:
                odds1 = float(dict_surebet[frame].at[i, 'btts_x'].split('\n')[0])
                odds2 = float(dict_surebet[frame].at[i, 'btts_y'].split('\n')[1]) #här vet jag inte hur jag ska göra 
                teams = dict_surebet[frame].at[i, 'Teams_x'].split('\n')
                dict_1 = beat_brokers(odds1, odds2, tot_stake)
                print(str(i)+' '+'-'.join(teams)+ ' ----> '+ ' '.join('{}:{}'.format(x, y) for x,y in dict_1.items()))
        for i, value in enumerate(dict_surebet[frame]['sure_btts2']):
            if value<1:
                odds1 = float(dict_surebet[frame].at[i, 'btts_x'].split('\n')[1])
                odds2 = float(dict_surebet[frame].at[i, 'btts_y'].split('\n')[0])
                teams = dict_surebet[frame].at[i, 'Teams_x'].split('\n')
                dict_2 = beat_brokers(odds1, odds2, tot_stake)
                print(str(i) + ' ' + '-'.join(teams) + ' ----> ' + ' '.join('{}:{}'.format(x, y) for x, y in dict_2.items()))
    #gör för alla sex 