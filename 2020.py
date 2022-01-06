from bs4 import BeautifulSoup
import requests 
import pandas as pd 
headers = {'User Agent':'Mozilla/5.0'}

players = ['anthony-edwards-2', 'james-wiseman', 'patrick-williams-2', 'isaac-okoro', 'onyeka-okongwu', 'obadiah-toppin', 'jalen-smith', 
           'devin-vassell', 'tyrese-haliburton', 'kira-lewisjr', 'aaron-nesmith', 'cole-anthony', 'isaiah-stewart-2', 'josh-green-2',
           'saddiq-bey', 'precious-achiuwa', 'tyrese-maxey', 'zeke-nnaji', 'immanuel-quickley', 'payton-pritchard', 'udoka-azubuike', 
           'jaden-mcdaniels', 'malachi-flynn', 'desmond-bane', 'tyrell-terry', 'vernon-careyjr', 'daniel-oturu', 'xavier-tillman', 
           'tyler-bey', 'saben-lee', 'elijah-hughes', 'robert-woodard-2', 'tre-jones', 'nick-richards-2', 'jahmius-ramsey', 
           'jordan-nwora', 'cj-elleby', 'nico-mannion', 'isaiah-joe', 'skylar-mays', 'justinian-jessup', 'cassius-winston', 
           'cassius-stanley', 'jay-scrubb', 'grant-riller', 'reggie-perry-2', 'paul-reed-5', 'jalen-harris-2', 'sam-merrill']

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
        player = player.replace('-',' ').title()
        for char in player:
            if char.isdigit():
                player = player.replace(char, '')
        playerlist.append(player)
        
    except:
        continue
     
table.insert(0, "Name", playerlist)
print(table)



