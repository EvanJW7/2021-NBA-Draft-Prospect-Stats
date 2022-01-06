from bs4 import BeautifulSoup
import requests 
import pandas as pd 
headers = {'User Agent':'Mozilla/5.0'}

players = [
    'cade-cunningham', 'jalen-suggs','evan-mobley', 'franz-wagner', 'davion-mitchell', 
    'scottie-barnes','moses-moody', 'ziaire-williams', 'corey-kispert', 'tre-mann', 'ayo-dosunmu',
    'max-abmas', 'kai-jones', 'josh-christopher', 'nahshon-hyland', 'jaden-springer', 'cameron-thomas', 'miles-mcbride', 
    'johnny-juzang', 'charles-bassey', 'chris-duarte', 'james-bouknight', 'jeremiah-robinson-earl', 'sharife-cooper', 
    'dj-stewart', 'brandon-bostonjr', 'joel-ayayi', 'isaiah-livers', 'david-duke', 'dayron-sharpe', 'keon-johnson',
    'marcus-zegarowski', 'rj-nembhard', 'aaron-henry', 'mj-walker', 'jericho-sims', 'raiquan-gray','feron-hunt', 
    'yves-pons', 'matthew-hurt', 'trey-murphyiii', 'ochai-agbaji', 'joshua-primo', 'aaron-wiggins', 'olivier-sarr', 
    'kessler-edwards', 'neemias-queta', 'jason-preston', 'sandro-mamukelashvili', 'jt-thor', 'quentin-grimes',
    'sam-hauser', 'matthew-mayer', 'macio-teague', 'javonte-smart', 'dj-steward', 'luka-garza', 'matthew-mcclung', 
    'aamir-simms', 'trendon-watford', 'justin-champagnie', 'austin-reaves', 'makur-maker', 'julian-champagnie',
    'keve-aluma','dejon-jarreau', 'jaquori-mclaughlin', 'derek-culver', 'moussa-cisse', 'michael-devoe',
    'mckinley-wrightiv', 'isaiah-jackson-3', 'jalen-johnson-24']

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
        player_stats.append([td.getText() for td in soup.find('tr', id ='players_per_game.2021')])
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


