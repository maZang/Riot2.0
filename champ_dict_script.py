import json
import pandas as pd
import RiotConsts as Consts
import numpy as np

with open('champ_dict.json', 'r') as df:
	CHAMP_TO_MATRIX = json.load(df)
roles = {0: "Overall", 1: "Fighter", 2: "Mage", 3: "Marksman", 4: "Support", 5: "Tank"}
def main():
	data = _normalize_data(pd.read_csv("./data1.csv").values)
	fighter_data = _normalize_data(pd.read_csv('./role_dataFighter.csv').values)
	mage_data = _normalize_data(pd.read_csv('./role_dataMage.csv').values)
	marksman_data = _normalize_data(pd.read_csv('./role_dataMarksman.csv').values)
	support_data = _normalize_data(pd.read_csv('./role_dataSupport.csv').values)
	tank_data = _normalize_data(pd.read_csv('./role_dataTank.csv').values)
	data_list = [data, fighter_data, mage_data, marksman_data, support_data, tank_data]
	new_champ_dict = {}
	for row in range(0, data.shape[0]):
		champ_name = _get_name(row)
		new_champ_dict[champ_name] = {}
		total_games = data[row, Consts.BLACK_MARKET_FEATURES-1]
		for idx, data_table in enumerate(data_list):
			dict_data = {}
			dict_data['kills'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['kills']]
			dict_data['deaths'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['deaths']]
			dict_data['assists'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['assists']]
			dict_data['cs_min'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['cs_min']]
			dict_data['gold_min'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['gold_min']]
			dict_data['win_rate'] = data_table[row, len(Consts.STAT_TO_MATRIX) + Consts.VARIABLE_TO_MATRIX['win']]
			dict_data['percent_games_played'] = data_table[row, Consts.BLACK_MARKET_FEATURES-1]/total_games
			new_champ_dict[champ_name][roles[idx]] = dict_data
	with open('new_champ_dict.json', 'w') as fp:
		json.dump(new_champ_dict, fp)

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