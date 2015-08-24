from RiotAPI import RiotAPI
import json
import numpy as np
import RiotConsts as Consts 
import requests
from LRU_Cache import LRUCache

with open('champ_dict.json', 'r') as df:
	CHAMP_TO_MATRIX = json.load(df)

SHOW_MATRIX = True

#cache results of search
mastery_cache = LRUCache(130)
rune_cache = LRUCache(130)
item_cache = LRUCache(130)
champion_cache = LRUCache(130)

def main():
	api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
	#loading the NA match ids
	data = json.loads(open('./BILGEWATER/NA.json').read())
	csv_data = np.zeros(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES]) 
	data_col_base = len(Consts.STAT_TO_MATRIX)
	_fill_champ_id_range(csv_data, data_col_base)
	match_num = 1
	for matchid in data:
		print("On match number " + str(match_num))
		match = api.get_match_info(matchid, {'includeTimeline': True})
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
			kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl = _parse_stats(champ['stats'], championID)
			cs_min, gold_min = _parse_timeline(champ['timeline'])
			atk_range = csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['atk_range']]
			#combination so it does not matter which order summoner spells are chosen
			spell1id = champ['spell2Id'] + champ['spell1Id']
			spell2id = champ['spell1Id'] * champ['spell2Id']
			#place data into matrix
			csv_data_delta = np.array([offense, defense, utility, kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl, 
				atk_range, cs_min, gold_min, spell1id, spell2id])
			csv_data[chmp_mtrx_index, data_col_base:data_col_base + len(Consts.VARIABLE_TO_MATRIX)] += csv_data_delta
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['offense']] += offense
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['defense']] += defense
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['utility']] += utility
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['kills']] += kills
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['deaths']] += deaths
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['assists']] += assists
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['phys_dmg']] += phys_dmg
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['mgc_dmg']] += mgc_dmg
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['true_dmg']] += true_dmg
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['dmg_taken']] += dmg_taken
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['team_jgl']] += team_jgl
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['enemy_jgl']] += enemy_jgl
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['cs_min']] += cs_min
			#csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['gold_min']] += gold_min
			#these methods input data directly into matrix
			csv_data = _parse_runes(champ.get('runes', []), csv_data, chmp_mtrx_index)
			csv_data = _parse_items(champ['stats'], csv_data, chmp_mtrx_index)
			
			#add 1 to champion counter	 
			csv_data[chmp_mtrx_index, Consts.BLACK_MARKET_FEATURES-1]+=1
		if SHOW_MATRIX:
			print(csv_data)
		match_num+=1
	np.savetxt('data.csv', csv_data, delimiter= ",", header = "Champion", comments = "")

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
	return kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl

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

def _parse_items(items, csv_data, champidx):
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
		#iterate through item stacks
		for key, value in cur_item['stats'].items():
			data_col = Consts.STAT_TO_MATRIX[key]
			csv_data[champidx, data_col]+= value
		item_cache.place(item, cur_item)
	return csv_data

if __name__ == "__main__":
	main()