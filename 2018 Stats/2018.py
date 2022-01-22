from bs4 import BeautifulSoup
import requests 
import pandas as pd 

headers = {'User Agent':'Mozilla/5.0'}

players = [
    'deandre-ayton', 'marvin-bagleyiii', 'jaren-jacksonjr', 'trae-young', 'mo-bamba', 'wendell-carterjr', 'collin-sexton',
    'kevin-knox', 'mikal-bridges', 'shai-gilgeous-alexander', 'miles-bridges', 'jerome-robinson', 'michael-porterjr', 
    'troy-brownjr', 'zhaire-smith', 'donte-divincenzo', 'lonnie-walkeriv', 'kevin-huerter', 'josh-okogie', 'grayson-allen',
    'chandler-hutchinson', 'aaron-holiday', 'moritz-wagner', 'landry-shamet', 'robert-williams', 'jacob-evans', 'omari-spellman', 
    'jevon-carter', 'jalen-brunson', 'devonte-graham', 'gary-trentjr', 'khyri-thomas', 'jarred-vanderbilt', 'bruce-brown',
    'hamidou-diallo', 'deanthony-melton', 'sviatoslav-mykhailiuk', 'keita-bates-diop', 'chimezie-metu', 'alize-johnson', 
    'tony-carr', 'vince-edwards', 'devon-hall', 'shake-milton', 'kostas-antetokounmpo'
    
    ]

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
        player_stats.append([td.getText() for td in soup.find('tr', id ='players_per_game.2018')])
        table = pd.DataFrame(player_stats, columns = header)
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

table["Player Grade"] = (table['PTS']*per40) + (table['TRB']*1.25*per40) + (table['AST']*2*per40) + (table['BLK']*2*per40) + (table['STL']*2*per40) + (table['3P']*7*per40)+ (table['FT%']*7) + (table['SOS']/2) + (table['3P%']*10)
table["Player Grade"] = table["Player Grade"]*1.2
table["Player Grade"] = (round(table["Player Grade"]))
table["Player Grade"]= table["Player Grade"].astype(int)
                        
table = table.sort_values(by= "Player Grade", ascending=False)
table.insert(4, 'SoS', table['SOS'])
table.reset_index(drop = True, inplace=True)
import numpy as np
table.index = np.arange(1, len(table)+1)
del table['SOS']
print(table)