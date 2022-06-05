from bs4 import BeautifulSoup
import requests 
import pandas as pd 
headers = {'User Agent':'Mozilla/5.0'}

players = ['paolo-banchero', 'jabari-smith-2', 'jonathan-davis-3', 'ej-liddell', 'julian-champagnie',
           'jamaree-bouyea', 'keon-ellis', 'kennedy-chandler', 'orlando-robinson', 'bryce-mcgowens',
           'blake-wesley', 'christian-koloko', 'kendall-brown', 'chet-holmgren', 'jaden-ivey', 
           'bennedict-mathurin', 'max-christie', 'patrick-baldwinjr', 'tyty-washingtonjr', 'jalen-duren', 
           'malaki-branham', 'jd-notae', 'keegan-murray', 'wendell-moorejr', 'jeremy-sochan', 
           'trevion-williams', 'ochai-agbaji', 'mark-williams-7', 'trayce-jackson-davis', 
           'jaime-jaquezjr', 'johnny-juzang', 'jahvon-quinerly', 'matthew-mayer', 'trevor-keels',  
           'walker-kessler', 'kameron-mcgusty', 'michael-devoe',  'iverson-molinar', 'keve-aluma', 
           'christian-braun','tyson-etienne', 'alex-barcello', 'max-abmas', 'kevin-obanor', 'brady-manek', 
           'izaiah-brockington', 'jd-davison', 'aj-griffin', 'tari-eason','jabari-walker', 'scotty-pippenjr']

player_stats = []
playerlist = []
year_list = []
age_list = []

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
    try:
        url = f'https://www.google.com/search?q={player}+basketball+birth+date'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        age = (soup.findAll('div', class_ = 'BNeawe iBp4i AP7Wnd')[0])
        for x in age:
            x = x.text
        x = x.replace(',','').split()
        months = {
            'Janurary': '1',
            'February': '2',
            'March': '3',
            'April': '4',
            'May': '5',
            'June': '6',
            'July': '7',
            'August': '8',
            'September': '9',
            'October': '10',
            'November': '11',
            'December': '12'
        } 
        birth_date = months[x[0]]+ '-' + x[1] + '-' + x[2]
        draft_date = '7-1-2022'
        import datetime 
        birth_date_final = datetime.datetime.strptime(birth_date, '%m-%d-%Y')  
        draft_date_final = datetime.datetime.strptime(draft_date, '%m-%d-%Y')

        age_on_draft_night = draft_date_final - birth_date_final
        age = round(age_on_draft_night.days/365, 1)
        age_list.append(age)
        year = round(((1-(age/35))*2.33), 2)
        year_list.append(year)
        
    except:
        age_list.append("No data")
        year_list.append(1)

age_list[1] = 19.1
year_list[1] = 1.07
age_list[2] = 20.3
year_list[2] = .96
age_list[3] = 21.6
year_list[3] = .83
age_list[4] = 21.0 
year_list[4] = .89
age_list[5] = 23.0 
year_list[5] = .69
age_list[6] = 22.5 
year_list[6] = .74
age_list[7] = 19.7 
year_list[7] = 1.01
age_list[8] = 22.0 
year_list[8] = .79
age_list[9] = 19.7 
year_list[9] = 1.01
age_list[10] = 19.3
year_list[10] = 1.05
age_list[11] = 22.4
year_list[11] = .75
age_list[12] = 19.2
year_list[12] = 1.06

table.insert(0, "Name", playerlist)
table.insert(2, "Year", year_list)
table.insert(2, "Age", age_list)

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

table["Player Grade"] = ((table['PTS']) + (table['TRB']*1.25) + (table['AST']*2) +
(table['BLK']*2) + (table['STL']*3) + (table['3P']*2) + (table['3PA']) + (table['SOS']/2)) * table['Year']

table["Player Grade"] = table["Player Grade"]*1.75
table["Player Grade"] = (round(table["Player Grade"], 1))
table["Player Grade"]= table["Player Grade"].astype(float)
                        
table = table.sort_values(by= "Player Grade", ascending=False)
table.insert(5, 'SoS', table['SOS'])
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
del table['Year']
del table['TOV']
del table['PF']
print(table)
