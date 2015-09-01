import json
import ast

with open('team_dict.json', 'r') as df:
	data = json.load(df)
#printed using python script
champ_list = ['Bard', 'Nautilus', 'Singed', 'Gragas', 'Quinn', 'Shyvana', 'Sejuani', 'Garen', 'Heimerdinger', 'RekSai', 'Vladimir', 'Mordekaiser', 'Sion', 'Poppy', 'Aatrox', 'Leblanc', 'Thresh', 'Lulu', 'Elise', 'Zac', 'Nasus', 'Shaco', 'Diana', 'Rammus', 'Ashe', 'Maokai', 'Draven', 'Fiora', 'Udyr', 'Volibear', 'MasterYi', 'Varus', 'Malzahar', 'Trundle', 'Gnar', 'TahmKench', 'Ryze', 'Katarina', 'JarvanIV', 'Azir', 'Rengar', 'Pantheon', 'Cassiopeia', 'Zyra', 'Sona', 'Akali', 'Veigar', 'Syndra', 'Teemo', 'Zilean', 'Tryndamere', 'Kennen', 'Velkoz', 'Vi', 'Riven', 'Fizz', 'Orianna', 'Gangplank', 'Yorick', 'Karma', 'Twitch', 'Ahri', 'MissFortune', 'Xerath', 'Irelia', 'Viktor', 'Chogath', 'Skarner', 'Talon', 'Darius', 'Nami', 'Taric', 'Rumble', 'Sivir', 'MonkeyKing', 'TwistedFate', 'Hecarim', 'Yasuo', 'Lissandra', 'Kassadin', 'Vayne', 'Braum', 'Jinx', 'XinZhao', 'Khazix', 'Kalista', 'Soraka', 'Lux', 'Karthus', 'Kayle', 'Ezreal', 'Evelynn', 'Swain', 'Graves', 'Warwick', 'Malphite', 'Jax', 'Jayce', 'Tristana', 'Ziggs', 'Caitlyn', 'Shen', 'KogMaw', 'Blitzcrank', 'Alistar', 'Brand', 'Nocturne', 'Nunu', 'Lucian', 'Leona', 'Zed', 'Urgot', 'DrMundo', 'Ekko', 'Corki', 'Olaf', 'Nidalee', 'LeeSin', 'FiddleSticks', 'Amumu', 'Janna', 'Morgana', 'Galio', 'Annie', 'Anivia', 'Renekton']
champ_syn_dict = {}
for champ in champ_list:
	champ_syn_dict[champ] = {}
	for comp, stats in data.items():
		comp = list(ast.literal_eval(comp))
		#print(comp)
		for champs in comp:
			if champs != champ:
				if champs not in champ_syn_dict[champ]:
					champ_syn_dict[champ][champs] = stats
				else:
					win, game = stats
					prev_win, prev_game = champ_syn_dict[champ][champs]
					champ_syn_dict[champ][champs] = (win + prev_win, game + prev_game)
print(champ_syn_dict)
new_syn_dict = {}
for champ in champ_syn_dict:
	new_syn_dict[champ] = {}
	syn_dict = champ_syn_dict[champ]
	if len(syn_dict) == 0:
		continue
	total_wins = 0
	total_games = 0
	for member in syn_dict:
		win, game = syn_dict[member]
		total_games += game
		total_wins += win
		#don't do it if not enough data
		new_syn_dict[champ][member] = (win, game)
	new_syn_dict[champ][champ] = (total_wins, total_games)
complete_syn_dict = {}
for champ in new_syn_dict:
	complete_syn_dict[champ] = {}
	for member in new_syn_dict[champ]:
		win,game = new_syn_dict[champ][member]
		win_1, game_1 = new_syn_dict[champ][champ]
		win_2, game_2 = new_syn_dict[member][member]
		weighted_win_rate = (win_1/game_1 * (game_1)/(game_1 + game_2) + win_2/game_2 * game_2/(game_1 + game_2))
		if win/game >= 1.01*weighted_win_rate:
			complete_syn_dict[champ][member] = (win/game)/(weighted_win_rate)
with open('syn_dict.json', 'w') as df:
	json.dump(complete_syn_dict, df)


