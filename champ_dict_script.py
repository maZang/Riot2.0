import json
import pandas as pd
import RiotConsts as Consts
import numpy as np
import math

with open('champ_dict.json', 'r') as df:
	CHAMP_TO_MATRIX = json.load(df)
roles = {0: "Overall", 1: "Physical Bruiser", 2: "Magical Bruiser", 3: "Assassin", 4: "Jungler", 5: "Mage", 6: "Marksman", 7: "Support", 8: "Tank"}
def main():
	data = _normalize_data(pd.read_csv("./data1.csv").values)
	phys_data = _normalize_data(pd.read_csv('./role_dataPhysical Bruiser.csv').values)
	mgc_data = _normalize_data(pd.read_csv('./role_dataMagical Bruiser.csv').values)
	ass_data = _normalize_data(pd.read_csv('./role_dataAssassin.csv').values)
	jgl_data = _normalize_data(pd.read_csv('./role_dataJungler.csv').values)
	mage_data = _normalize_data(pd.read_csv('./role_dataMage.csv').values)
	marksman_data = _normalize_data(pd.read_csv('./role_dataMarksman.csv').values)
	support_data = _normalize_data(pd.read_csv('./role_dataSupport.csv').values)
	tank_data = _normalize_data(pd.read_csv('./role_dataTank.csv').values)
	data_list = [data, phys_data, mgc_data, ass_data, jgl_data, mage_data, marksman_data, support_data, tank_data]
	new_champ_dict = {}
	new_champ_dict_ovl = {}
	play_data = {}
	for row in range(0, data.shape[0]):
		champ_name = _get_name(row)
		new_champ_dict[champ_name] = []
		play_data[champ_name] = []
		total_games = data[row, Consts.BLACK_MARKET_FEATURES-1]
		for idx, data_table in enumerate(data_list):
			dict_data = {}
			play_data_item = {}
			dict_data['kills'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['kills']]
			dict_data['deaths'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['deaths']]
			dict_data['assists'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['assists']]
			dict_data['cs_min'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['cs_min']]
			dict_data['gold_min'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['gold_min']]
			dict_data['win_rate'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['win']]
			play_data_item['value'] = data_table[row, Consts.BLACK_MARKET_FEATURES-1]/total_games
			dict_data['role'] = roles[idx]
			play_data_item['label'] = roles[idx]
			if idx == 0:
				spell_1 = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['spell1id']]
				spell_2 = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['spell2id']]
				spell_1, spell_2 = get_summoner_spells(spell_1, spell_2)
				dict_data['spell1'] = spell_1
				dict_data['spell2'] = spell_2
				dict_data['health_built'] = data_table[row, Consts.STAT_TO_MATRIX['FlatHPPoolMod']]
				dict_data['ad_built'] = data_table[row, Consts.STAT_TO_MATRIX['FlatPhysicalDamageMod']]
				dict_data['ap_built'] = data_table[row, Consts.STAT_TO_MATRIX['FlatMagicDamageMod']]
				new_champ_dict_ovl[champ_name] = dict_data 
			else:
				new_champ_dict[champ_name].append(dict_data)
				play_data[champ_name].append(play_data_item)
	with open('new_champ_dict.json', 'w') as fp:
		json.dump(new_champ_dict, fp)
	with open('new_champ_dict_ovl.json', 'w') as fp:
		json.dump(new_champ_dict_ovl, fp)
	with open('play_data.json', 'w') as fp:
		json.dump(play_data, fp)

def get_summoner_spells(spell1, spell2):
	maths = spell1 ** 2 - 4 * spell2
	if maths < 0:
		return "Flash", "Ignite"
	x = 1/2 * (spell1 - math.sqrt(spell1 ** 2  - 4 * spell2))
	y = 1/2 * (math.sqrt(spell1 ** 2- 4 * spell2)  + spell1)
	x = rounding(x)
	y = rounding(y)
	options = {1: "SummonerBoost", 12: "SummonerTeleport", 14: "SummonerDot", 6: "SummonerHaste", 7: "SummonerHeal", 11: "SummonerSmite", 3: "SummonerExhaust", 13: "SummonerMana", 2: "SummonerClairvoyance", 21: "SummonerBarrier", 4: "SummonerFlash"}
	return options[x], options[y]

def rounding(num):
	if num > 0 and num < 1.5:
		return 1
	if num < 2.5 and num >= 1.5:
		return 2
	if num < 3.5 and num >= 2.5:
		return 3
	if num < 5 and num >= 3.5:
		return 4
	if num >= 5 and num < 6.5:
		return 6
	if num >= 6.5 and num < 9:
		return 7
	if num >= 9 and num < 11.5:
		return 11
	if num >= 11.5 and num < 12.5:
		return 12
	if num >= 12.5 and num < 13.5:
		return 13
	if num >= 13.5 and num < 17.5:
		return 14
	else:
		return 21

def _normalize_data(data):
	num_games = data[:, Consts.BLACK_MARKET_FEATURES - 1]
	#champs with 0 games
	bad_values = []
	for i, j in enumerate(num_games):
		if j == 0:
			bad_values.append(i)
	#replace bad rows with 0s
	zero_fill = np.zeros(shape=[1, Consts.BLACK_MARKET_FEATURES - 1])
	zero_fill = np.concatenate((zero_fill, np.reshape(np.array([1]), (1, 1))), axis = 1)
	for row in bad_values:
		data[row] = zero_fill
	for col in range(1, data.shape[1] - 1):
		data[:, col] = np.divide(data[:, col], num_games)
	return data 

def _get_name(num):
	for k, v in CHAMP_TO_MATRIX.items():
		if v == num:
			return k 
	return "Error"

if __name__ == "__main__":
	main()