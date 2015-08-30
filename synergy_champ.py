import json
import ast

#test data 
team_comps = {'("Garen", "Lux", "Jinx", "Vi", "Lulu")': (10, 25), '("Lulu", "Jinx", "Garen", "Vi", "KogMaw")': (11, 30)}
with open('team_dict.json', 'w') as fp:
	json.dump(team_comps, fp)
data = json.loads(open('team_dict.json').read())
print(data)
#printed using python script
champ_list = ['Bard', 'Nautilus', 'Singed', 'Gragas', 'Quinn', 'Shyvana', 'Sejuani', 'Garen', 'Heimerdinger', 'RekSai', 'Vladimir', 'Mordekaiser', 'Sion', 'Poppy', 'Aatrox', 'Leblanc', 'Thresh', 'Lulu', 'Elise', 'Zac', 'Nasus', 'Shaco', 'Diana', 'Rammus', 'Ashe', 'Maokai', 'Draven', 'Fiora', 'Udyr', 'Volibear', 'MasterYi', 'Varus', 'Malzahar', 'Trundle', 'Gnar', 'TahmKench', 'Ryze', 'Katarina', 'JarvanIV', 'Azir', 'Rengar', 'Pantheon', 'Cassiopeia', 'Zyra', 'Sona', 'Akali', 'Veigar', 'Syndra', 'Teemo', 'Zilean', 'Tryndamere', 'Kennen', 'Velkoz', 'Vi', 'Riven', 'Fizz', 'Orianna', 'Gangplank', 'Yorick', 'Karma', 'Twitch', 'Ahri', 'MissFortune', 'Xerath', 'Irelia', 'Viktor', 'Chogath', 'Skarner', 'Talon', 'Darius', 'Nami', 'Taric', 'Rumble', 'Sivir', 'MonkeyKing', 'TwistedFate', 'Hecarim', 'Yasuo', 'Lissandra', 'Kassadin', 'Vayne', 'Braum', 'Jinx', 'XinZhao', 'Khazix', 'Kalista', 'Soraka', 'Lux', 'Karthus', 'Kayle', 'Ezreal', 'Evelynn', 'Swain', 'Graves', 'Warwick', 'Malphite', 'Jax', 'Jayce', 'Tristana', 'Ziggs', 'Caitlyn', 'Shen', 'KogMaw', 'Blitzcrank', 'Alistar', 'Brand', 'Nocturne', 'Nunu', 'Lucian', 'Leona', 'Zed', 'Urgot', 'DrMundo', 'Ekko', 'Corki', 'Olaf', 'Nidalee', 'LeeSin', 'FiddleSticks', 'Amumu', 'Janna', 'Morgana', 'Galio', 'Annie', 'Anivia', 'Renekton']
champ_syn_dict = {}
for champ in champ_list:
	champ_syn_dict[champ] = {}
	for comp, stats in data.items():
		comp = list(ast.literal_eval(comp))
		if champ not in comp:
			break
		for champs in comp:
			if champs != champ:
				if champs not in champ_syn_dict[champ]:
					champ_syn_dict[champ][champs] = stats
				else:
					win, game = stats
					prev_win, prev_game = champ_syn_dict[champ][champs]
					champ_syn_dict[champ][champs] = (win + prev_win, game + prev_game)
print(champ_syn_dict)
compiled_syn_dict = {}
for champ in champ_syn_dict:
	compiled_syn_dict[champ] = {}
	syn_dict = champ_syn_dict[champ]
	if len(syn_dict) == 0:
		continue
	total_wins = 0
	total_games = 0
	new_syn_dict = {}
	for member in syn_dict:
		win, game = syn_dict[member]
		total_games += game
		total_wins += win
		#don't do it if not enough data
		if game > 30:
			new_syn_dict[member] = win/game
	win_rate = total_wins / total_games
	for member in new_syn_dict:
		if new_syn_dict[member] > win_rate:
			compiled_syn_dict[champ][member] = new_syn_dict[member]/win_rate
print(compiled_syn_dict)


