from bs4 import BeautifulSoup
import requests 
import pandas as pd 
headers = {'User Agent':'Mozilla/5.0'}

players = ['paolo-banchero', 'jabari-smith-2', 'chet-holmgren', 'jaden-ivey', 'bennedict-mathurin', 
           'blake-wesley', 'bryce-mcgowens', 'max-christie', 'patrick-baldwinjr', 'tyty-washingtonjr',
           'jalen-duren', 'jonathan-davis-3', 'julian-strawther', 'kendall-brown', 'caleb-houstan', 
           'aminu-mohammed', 'kennedy-chandler', 'keegan-murray', 'wendell-moorejr', 'dereon-seabron',
           'ochai-agbaji', 'mark-williams-7', 'caleb-love', 'trayce-jackson-davis', 'terrence-shannonjr',
           'jamaree-bouyea', 'jaime-jaquezjr', 'johnny-juzang', 'jahvon-quinerly', 'matthew-mayer', 
           'trevor-keels', 'orlando-robinson', 'taevion-kinsey', 'anthony-duruji', 'keon-ellis',
           'julian-champagnie', 'ej-liddell', 'michael-devoe', 'andrew-nembhard', 'oscar-tshiebwe',
           'iverson-molinar', 'jahmir-young', 'tyson-etienne', 'alex-barcello', 'max-abmas', 'kevin-obanor',
           'brady-manek', 'izaiah-brockington', 'moussa-diabate']

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
        player_stats.append([td.getText() for td in soup.find('tr', id ='players_per_game.2022')])
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
print(table)