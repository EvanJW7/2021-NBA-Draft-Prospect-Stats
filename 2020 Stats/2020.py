from bs4 import BeautifulSoup
import requests 
import pandas as pd 
headers = {'User Agent':'Mozilla/5.0'}

players = ['anthony-edwards-2', 'james-wiseman', 'patrick-williams-2', 'isaac-okoro', 'onyeka-okongwu', 
           'obadiah-toppin', 'jalen-smith', 'devin-vassell', 'tyrese-haliburton', 'kira-lewisjr', 'aaron-nesmith', 
           'cole-anthony', 'isaiah-stewart-2', 'josh-green-2','saddiq-bey', 'precious-achiuwa', 'tyrese-maxey', 
           'zeke-nnaji', 'immanuel-quickley', 'payton-pritchard',  'udoka-azubuike', 'jaden-mcdaniels', 
           'malachi-flynn', 'desmond-bane', 'tyrell-terry', 'vernon-careyjr', 'daniel-oturu', 'xavier-tillman', 
           'tyler-bey', 'saben-lee', 'elijah-hughes', 'robert-woodard-2', 'tre-jones', 'nick-richards-2', 
           'jahmius-ramsey', 'jordan-nwora', 'cj-elleby', 'nico-mannion', 'isaiah-joe', 'skylar-mays', 
           'justinian-jessup', 'cassius-winston', 'cassius-stanley', 'jay-scrubb', 'grant-riller', 'reggie-perry-2', 
           'paul-reed-5', 'jalen-harris-2', 'sam-merrill']

player_stats = []
playerlist = []

for player in players:
    try:
        if player[-1].isdigit():
            url = f'https://www.sports-reference.com/cbb/players/{player}.html'
        else:
            url = f'https://www.sports-reference.com/cbb/players/{player}-1.html'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        header = [th.getText() for th in soup.findAll('tr', limit = 2)[0].findAll('th')]
        rows = soup.findAll('tr')
        player_stats.append([td.getText() for td in soup.find('tr', id ='players_per_game.2020')])
        table = pd.DataFrame(player_stats, columns = header) 
        for i in player_stats:
            if i[14] == '':
                i[14] = str(0.0)
        
        player = player.replace('-',' ').title()
        if player[-1].isdigit():
            player = player[:-2]
        if player[-2:] == 'jr':
            player = player.replace('jr', ' Jr')
        playerlist.append(player)
        
    except:
        continue
  
table.insert(0, "Name", playerlist)
table['MP'] = table['MP'].astype(float)
table['PTS'] = table['PTS'].astype(float)
table['AST'] = table['AST'].astype(float)
table['TRB'] = table['TRB'].astype(float)
table['BLK'] = table['BLK'].astype(float)
table['STL'] = table['STL'].astype(float)
table['3P'] = table['3P'].astype(float)
table['3PA'] = table['3PA'].astype(float)
table['TOV'] = table['TOV'].astype(float)
table['SOS'] = table['SOS'].astype(float)
table['PF'] = table['PF'].astype(float)
table['FT%'] = table['FT%'].astype(float)
table['3P%'] = table['3P%'].astype(float)

per40 = 40/table['MP']

table["Player Grade"] = ((table['PTS']*per40) + (table['TRB']*1.25*per40) + (table['AST']*2*per40) +
(table['BLK']*3*per40) + (table['STL']*3*per40) + (table['3P']*7*per40)+ (table['FT%']*7) + (table['SOS']) + 
(table['3P%']*10))  

table["Player Grade"] = table["Player Grade"]*1.10
table["Player Grade"] = (round(table["Player Grade"]))
table["Player Grade"]= table["Player Grade"].astype(int)
                        
table = table.sort_values(by= "Player Grade", ascending=False)
table.insert(4, 'SoS', table['SOS'])
table.reset_index(drop = True, inplace=True)
import numpy as np
table.index = np.arange(1, len(table)+1)
del table['SOS']
del table['Conf']
del table['ORB']
del table['DRB']
del table['GS']
del table['FG']
del table['FGA']
del table['FT']
del table['FTA']
del table['2P']
del table['2PA']
del table['2P%']
print(table)