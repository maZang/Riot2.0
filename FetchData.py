from RiotAPI import RiotAPI
import json
import numpy as np
import RiotConsts as Consts 
import requests

with open('champ_dict.json', 'r') as df:
	CHAMP_TO_MATRIX = json.load(df)

def main():
	#loading the NA match ids
	data = json.loads(open('./BILGEWATER/NA.json').read())
	csv_data = np.empty(shape=[Consts.BLACK_MARKET_CHAMPIONS, Consts.BLACK_MARKET_FEATURES]) 
	data_col_base = len(Consts.STAT_TO_MATRIX)
	_fill_champ_names(csv_data)
	for matchid in data:
		match = api.get_match_info(matchid, {'includeTimeline': True})
		for champ in match['paricipants']:
			#get champ id and name
			championID = champ['stats']['championId']
			champ_name = _get_champ_name(championID)
			chmp_mtrx_index = CHAMP_TO_MATRIX[champ_name]
			#these methods return values which must then be input into the matrix
			offense, defense, utility = _parse_masteries(champ['masteries'])
			kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl, atk_range = _parse_stats(champ['stats'], championID)
			cs_min, gold_min = _parse_timeline(champ['timeline'])
			#place data into matrix
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['offense']] += offense
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['defense']] += defense
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['utility']] += utility
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['kills']] += kills
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['deaths']] += deaths
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['assists']] += assists
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['phys_dmg']] += phys_dmg
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['mgc_dmg']] += mgc_dmg
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['true_dmg']] += true_dmg
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['dmg_taken']] += dmg_taken
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['team_jgl']] += team_jgl
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['enemy_jgl']] += enemy_jgl
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['atk_range']] += atk_range
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['cs_min']] += cs_min
			csv_data[chmp_mtrx_index][data_col_base+Consts.VARIABLE_TO_MATRIX['gold_min']] += gold_min
			#these methods input data directly into matrix
			csv_data = _parse_runes(champ['runes'], csv_data, chmp_mtrx_index)
			csv_data = _parse_items(champ['stats'], csv_data, chmp_mtrx_index)
			#combination so it does not matter which order summoner spells are chosen
			spell1id = champ['spell2Id'] + champ['spell1Id']
			spell2id = champ['spell1Id'] * champ['spell2Id']
			#add 1 to champion counter	 
			csv_data[chmp_mtrx_index, Consts.BLACK_MARKET_FEATURES-1]+=1

def _fill_champ_names(csv_data):
	for col in range(csv_data.shape[0]):
		name = _get_name(col)
		csv_data[col][0] = name

def _get_name(num):
	for k, v in CHAMP_TO_MATRIX:
		if v == num:
			return k 
	return "Error"

def _get_champ_name(champid):
	api = RiotAPI('5692a80d-37e8-476a-8b37-7995789d9bf7')
	name = api.get_champ_by_id(champid)['name']
	return name

def _parse_masteries(masteries):
	api = RiotAPI('5692a80d-37e8-476a-8b37-7995789d9bf7')
	offense = 0
	defense = 0
	utility = 0
	for mastery in masteries:
		masteryId = mastery['masteryId']
		cur_mastery = api.get_mastery_by_id(masteryId, {'masteryData': 'masteryTree'})
		if cur_mastery['masteryTree'] == 'Offense':
			offense += mastery['rank']
		elif cur_mastery['masteryTree'] == 'Defense':
			defense += mastery['rank']
		else:
			utility += mastery['rank']
	if (offense + defense + utility) > 30:
		print("Error with masteries!")
	return offense, defense, utility

def _parse_stats(stats, champid):
	api = RiotAPI('5692a80d-37e8-476a-8b37-7995789d9bf7')
	kills = stats['kills']
	deaths = stats['deaths']
	assists = stats['assits']
	phys_dmg = stats['physicalDamageDealtToChampions']
	mgc_dmg = stats['magicDamageDealtToChampions']
	true_dmg = stats['trueDamageDealtToChampions']
	dmg_taken = stats['totalDamageTaken']
	team_jgl = stats['neutralMinionsKilledTeamJungle']
	enemy_jgl = stats['neutralMinionsKilledEnemyJungle']
	championid = stats['championId']
	champ = api.get_champ_by_id(championId, {'champData': 'stats'})
	atk_range = champ['stats']['attackrange']
	return kills, deaths, assists, phys_dmg, mgc_dmg, true_dmg, dmg_taken, team_jgl, enemy_jgl, atk_range

def _parse_timeline(timeline):
	cs_min_dict = timeline['creepsPerMinDeltas']
	gold_min_dict = timeline['goldPerMinDeltas']
	#both dictionaries should have the same lengths
	if len(cs_min_dict) != len(gold_min_dict):
		print("Error with timeline!")
	cs_min = cs_min_dict['zeroToTen']
	gold_min = gold_min_dict['zeroToTen']
	#variable game lenghts -- check if value is even in the dictionary
	if cs_min_dict.has_key('tenToTwenty'):
		cs_min += cs_min_dict['tenToTwenty']
		gold_min += gold_min_dict['tenToTwenty']
	if cs_min_dict.has_key('twentyToThirty'):
		cs_min += cs_min_dict['twentyToThirty']
		gold_min += gold_min_dict['twentyToThirty']
	if cs_min_dict.has_key('thirtyToEnd'):
		cs_min += cs_min_dict['thirtyToEnd']
		gold_min += gold_min_dict['thirtyToEnd']
	#take average of all the values
	return cs_min/len(cs_min_dict), gold_min/len(gold_min_dict)

def _parse_runes(runes, csv_data, champidx):
	api = RiotAPI('5692a80d-37e8-476a-8b37-7995789d9bf7')
	for rune in runes:
		runeId = rune['runeId']
		cur_rune = api.get_rune_by_id(item, {'runeData': 'stats'})
		for key, value in cur_rune['stats']:
			data_col = Consts.STAT_TO_MATRIX[key]
			csv_data[champidx][data_col] += value * rune['rank']
	return csv_data

def _parse_items(items, csv_data, champidx):
	#trinket not taken into consideration
	api = RiotAPI('5692a80d-37e8-476a-8b37-7995789d9bf7')
	item1 = items['items0']
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
		cur_item = api.get_item_by_id(item, {'itemData': 'stats'})
		#iterate through item stacks
		for key, value in cur_item['stats']:
			data_col = Consts.STAT_TO_MATRIX[key]
			csv_data[champidx, data_col]+= value
	return csv_data

if __name__ == "__main__":
	main()