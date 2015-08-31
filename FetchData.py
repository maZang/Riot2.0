from RiotAPI import RiotAPI
import json
import numpy as np
import RiotConsts as Consts 
import requests
from LRU_Cache import LRUCache
import k_means_learning as KLearn

with open('champ_dict.json', 'r') as df:
	CHAMP_TO_MATRIX = json.load(df)

SHOW_MATRIX = True

#cache results of search
mastery_cache = LRUCache(150)
rune_cache = LRUCache(150)
item_cache = LRUCache(150)
champion_cache = LRUCache(126)

def main():
	#np.set_printoptions(threshold=np.inf)
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	api_euw = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2', Consts.REGIONS['europe_west'])
	api_eune = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2', Consts.REGIONS['europe_nordic_and_east'])
	#loading the NA match ids
	data = json.loads(open('./BILGEWATER/EUNE.json').read())
	data += json.loads(open('./BILGEWATER/EUW.json').read())
	data += json.loads(open('./BILGEWATER/NA.json').read())
	csv_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	pop_items = make_items_dict()
	pop_spells = make_spells_dict()
	team_comps = {}
	data_col_base = len(Consts.STAT_TO_MATRIX)
	_fill_champ_id_range(csv_data, data_col_base)
	match_num = 1
	for matchid in data:
		print("On match number " + str(match_num))
		if match_num <= 10000:
			#print(matchid)
			match = api_eune.get_match_info(matchid, {'includeTimeline': True})
		elif match_num <= 20000:
			match = api_euw.get_match_info(matchhid, {'includeTimeline': True})
		else: 
			match = api.get_match_info(matchhid, {'includeTimeline': True})
		win_team = []
		lose_team = []
		for champ in match['participants']:
			#get champ id and name
			championID = champ['championId']
			champ_name = champion_cache.find(championID)
			if champ_name is False:
				champ_name = api.get_champ_by_id(championID)['key']
			champion_cache.place(championID, champ_name)
			chmp_mtrx_index = CHAMP_TO_MATRIX[champ_name]
			#these methods return values which must then be input into the matrix
			offense, defense, utility = _parse_masteries(champ.get('masteries', []))
			kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl, win = _parse_stats(champ['stats'], championID)
			cs_min, gold_min = _parse_timeline(champ['timeline'])
			#combination so it does not matter which order summoner spells are chosen
			spell1id = champ['spell2Id'] + champ['spell1Id']
			spell2id = champ['spell1Id'] * champ['spell2Id']
			if champ['spell2Id'] in pop_spells[champ_name]:
				pop_spells[champ_name]['spell2Id'] += 1
			else:
				pop_spells[champ_name]['spell2Id'] = 1
			if champ['spell1Id'] in pop_spells[champ_name]:
				pop_spells[champ_name]['spell1Id'] += 1
			else:
				pop_spells[champ_name]['spell1Id'] = 1
			#place data into matrix
			#attack range not changed because data is normalized anyway
			csv_data_delta = np.array([offense, defense, utility, kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl, 
				0, cs_min, gold_min, spell1id, spell2id, win])
			csv_data[chmp_mtrx_index, data_col_base + 1:data_col_base + len(Consts.VARIABLE_TO_MATRIX) + 1] += csv_data_delta
			#these methods input data directly into matrix
			csv_data = _parse_runes(champ.get('runes', []), csv_data, chmp_mtrx_index)
			csv_data = _parse_items(champ['stats'], csv_data, chmp_mtrx_index, pop_items, True)
			
			#add 1 to champion counter	 
			csv_data[chmp_mtrx_index, Consts.BLACK_MARKET_FEATURES-1]+=1

			#add to team list
			if win == 1:
				win_team.append(champ_name)
			else:
				lose_team.append(champ_name)
		if SHOW_MATRIX:
			print(csv_data)
		win_team = tuple(sorted(win_team))
		#print(win_team)
		lose_team = tuple(sorted(lose_team))
		#print(lose_team)
		team_comps = add_to_team_comps(win_team, lose_team, team_comps)
		#print(team_comps)
		match_num+=1
	np.savetxt('data.csv', csv_data, delimiter= ",", comments = "")
	with open('item_dict.json', 'w') as fp:
		json.dump(pop_items, fp)
	with open('team_dict.json', 'w') as fp:
		json.dump(team_comps, fp)
	with open('spell_dict.json', 'w') as fp:
		json.dump(pop_spells, fp)

def second_main():
	#np.set_printoptions(threshold=np.inf)
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	api_euw = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2', Consts.REGIONS['europe_west'])
	api_eune = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2', Consts.REGIONS['europe_nordic_and_east'])
	api_kr = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2', Consts.REGIONS['korea'])
	#loading the NA match ids
	data = json.loads(open('./BILGEWATER/EUW.json').read())
	data += json.loads(open('./BILGEWATER/KR.json').read())
	data += json.loads(open('./BILGEWATER/NA.json').read())
	data_col_base = len(Consts.STAT_TO_MATRIX)
	#initialize different arrays
	marksman_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	support_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	mage_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	tank_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	phys_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	mgc_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	jgler_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	ass_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES])
	data_list = {'Magical Bruiser': mgc_data, 'Assassin': ass_data, 'Jungler': jgler_data, 'Marksman': marksman_data, 'Support': support_data, 'Mage': mage_data, 'Tank': tank_data, 'Physical Bruiser': phys_data}
	for role in data_list:
		_fill_champ_id_range(data_list[role], data_col_base)
	#initialize k-cluster
	kmean, scaler = KLearn.get_k_learn()
	match_num = 1
	for matchid in data:
		print("On match number " + str(match_num))
		if match_num <= 10000:
			#print(matchid)
			match = api_euw.get_match_info(matchid, {'includeTimeline': True})
		elif match_num <= 20000:
			match = api_kr.get_match_info(matchhid, {'includeTimeline': True})
		else: 
			match = api.get_match_info(matchhid, {'includeTimeline': True})
		for champ in match['participants']:
			champ_data = np.zeros(shape=[1, Consts.BLACK_MARKET_FEATURES])
			#get champ id and name
			championID = champ['championId']
			champ_name = champion_cache.find(championID)
			if champ_name is False:
				champ_name = api.get_champ_by_id(championID)['key']
			champion_cache.place(championID, champ_name)
			chmp_mtrx_index = CHAMP_TO_MATRIX[champ_name]
			#these methods return values which must then be input into the matrix
			offense, defense, utility = _parse_masteries(champ.get('masteries', []))
			kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl, win = _parse_stats(champ['stats'], championID)
			cs_min, gold_min = _parse_timeline(champ['timeline'])
			#combination so it does not matter which order summoner spells are chosen
			spell1id = champ['spell2Id'] + champ['spell1Id']
			spell2id = champ['spell1Id'] * champ['spell2Id']
			#place data into matrix
			#attack range not changed because data is normalized anyway
			data_delta = np.array([offense, defense, utility, kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl, 
				0, cs_min, gold_min, spell1id, spell2id, win])
			champ_data[0, data_col_base + 1:data_col_base + len(Consts.VARIABLE_TO_MATRIX) + 1] += data_delta
			#these methods input data directly into matrix
			champ_data = _parse_runes(champ.get('runes', []), champ_data, 0)
			champ_data = _parse_items(champ['stats'], champ_data, 0, {}, False)
			#add 1 to champion counter	 
			champ_data[0, Consts.BLACK_MARKET_FEATURES-1]+=1
			cluster_num = find_cluster(kmean, scaler, champ_data)
			data_list[KLearn.roles[cluster_num]][chmp_mtrx_index] += champ_data.flatten()
		match_num+=1
	for role in data_list:
		np.savetxt('role_data' + role + '.csv', data_list[role], delimiter= ",", comments = "")

def find_cluster(kmean, scaler, champ_data):
	scaled_data = champ_data[:, 1:Consts.BLACK_MARKET_FEATURES-2]
	scaled_data = scaler.transform(scaled_data)
	return kmean.predict(scaled_data)[0]

def add_to_team_comps(win_team, lose_team, team_comps):
	if str(win_team) not in team_comps:
		team_comps[str(win_team)] = (1, 1)
	else:
		win, games = team_comps[str(win_team)]
		team_comps[str(win_team)] = (win + 1, games + 1)
	if str(lose_team) not in team_comps:
		team_comps[str(lose_team)]= (0, 1)
	else:
		win, games = team_comps[str(lose_team)]
		team_comps[str(lose_team)] = (win, games + 1)
	return team_comps

def make_items_dict():
	champ_dict = {}
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	champs = api.get_all_champs()
	for champ in champs['data'].keys():
		champ_dict[champ] = {}
	return champ_dict

def make_spells_dict():
	champ_dict = {}
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	champs = api.get_all_champs()
	for champ in champs['data'].keys():
		champ_dict[champ] = {}
	return champ_dict

def _fill_champ_id_range(csv_data, data_col_base):
	#fill out champ ids and attack range
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	champs = api.get_all_champs({'champData': 'stats'})
	for col in range(csv_data.shape[0]):
		name = _get_name(col)
		csv_data[col][0] = champs['data'][name]['id']
		csv_data[col][data_col_base + Consts.VARIABLE_TO_MATRIX['atk_range']] = champs['data'][name]['stats']['attackrange']

def _get_name(num):
	for k, v in CHAMP_TO_MATRIX.items():
		if v == num:
			return k 
	return "Error"

def _parse_masteries(masteries):
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	offense = 0
	defense = 0
	utility = 0
	for mastery in masteries:
		masteryId = mastery['masteryId']
		cur_mastery = mastery_cache.find(masteryId)
		if cur_mastery is False:
			cur_mastery = api.get_mastery_by_id(masteryId, {'masteryData': 'masteryTree'})
		#	print('Mastery not in cache')
		#else:
		#	print('Mastery in cache')
		if cur_mastery['masteryTree'] == 'Offense':
			offense += mastery['rank']
		elif cur_mastery['masteryTree'] == 'Defense':
			defense += mastery['rank']
		elif cur_mastery['masteryTree'] == 'Utility':
			utility += mastery['rank']
		mastery_cache.place(masteryId, cur_mastery)
	if (offense + defense + utility) > 30:
		print("Error with masteries!")
	return offense, defense, utility

def _parse_stats(stats, champid):
	kills = stats['kills']
	deaths = stats['deaths']
	assists = stats['assists']
	phys_dmg = stats['physicalDamageDealtToChampions']
	mgc_dmg = stats['magicDamageDealtToChampions']
	true_dmg = stats['trueDamageDealtToChampions']
	dmg_taken = stats['totalDamageTaken']
	team_jgl = stats['neutralMinionsKilledTeamJungle']
	enemy_jgl = stats['neutralMinionsKilledEnemyJungle']
	winner = stats['winner']
	if winner is False:
		win = 0
	else:
		win = 1
	return kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl, win

def _parse_timeline(timeline):
	cs_min_dict = timeline['creepsPerMinDeltas']
	gold_min_dict = timeline['goldPerMinDeltas']
	#both dictionaries should have the same lengths
	if len(cs_min_dict) != len(gold_min_dict):
		print("Error with timeline!")
	cs_min = cs_min_dict['zeroToTen']
	gold_min = gold_min_dict['zeroToTen']
	#variable game lenghts -- check if value is even in the dictionary
	if 'tenToTwenty' in cs_min_dict:
		cs_min += cs_min_dict['tenToTwenty']
		gold_min += gold_min_dict['tenToTwenty']
	if 'twentyToThirty' in cs_min_dict:
		cs_min += cs_min_dict['twentyToThirty']
		gold_min += gold_min_dict['twentyToThirty']
	if 'thirtyToEnd' in cs_min_dict:
		cs_min += cs_min_dict['thirtyToEnd']
		gold_min += gold_min_dict['thirtyToEnd']
	#take average of all the values
	return cs_min/len(cs_min_dict), gold_min/len(gold_min_dict)

def _parse_runes(runes, csv_data, champidx):
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	for rune in runes:
		runeId = rune['runeId']
		cur_rune = rune_cache.find(runeId)
		if cur_rune is False:
			cur_rune = api.get_rune_by_id(runeId, {'runeData': 'stats'})
			if cur_rune is False:
				return csv_data
		for key, value in cur_rune['stats'].items():
			data_col = Consts.STAT_TO_MATRIX[key]
			csv_data[champidx][data_col] += value * rune['rank']
		rune_cache.place(runeId, cur_rune)
	return csv_data

def _parse_items(items, csv_data, champidx, pop_items, itemDict):
	#trinket not taken into consideration
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	item1 = items['item0']
	item2 = items['item1']
	item3 = items['item2']
	item4 = items['item3']
	item5 = items['item4']
	item6 = items['item5']
	itemList = [item1, item2, item3, item4, item5, item6]
	for item in itemList:
		#make sure an item is there
		if item == 0:
			continue 
		#get item data
		cur_item = item_cache.find(item)
		if cur_item is False:
			cur_item = api.get_item_by_id(item, {'itemData': 'stats'})
			if cur_item is False:
				return csv_data
		#iterate through item stats
		for key, value in cur_item['stats'].items():
			data_col = Consts.STAT_TO_MATRIX[key]
			csv_data[champidx, data_col]+= value
		item_cache.place(item, cur_item)
		#put item in item dict unless no itemDict
		if itemDict is False:
			return csv_data
		name = _get_name(champidx)
		item_dict = pop_items[name]
		if item not in item_dict:
			item_dict[item] = 1
		else:
			item_dict[item] += 1
	return csv_data

if __name__ == "__main__":
	#second_main()
	main()