import json 
import numpy as np
import pandas as pd
import RiotConsts as Consts

def main():
	new_item_dict = {}
	with open('item_dict.json', 'r') as df:
		pop_items= json.load(df)
	num_games = pd.read_csv("./data.csv", header=None).values[:, Consts.BLACK_MARKET_FEATURES-1]
	with open('champ_dict.json', 'r') as df:
		CHAMP_TO_MATRIX = json.load(df)
	for champ in pop_items:
		num_game = num_games[CHAMP_TO_MATRIX[champ]]
		new_item_list = []
		item_dict = pop_items[champ]
		for item in range(0, 10):
			item_idx, num_played = get_max_val_idx(item_dict)
			del item_dict[item_idx]
			percent_played = num_played/num_game
			new_item_list.append((item_idx, percent_played))
		new_item_dict[champ] = new_item_list
	with open('pop_item_dict.json', 'w') as fp:
		json.dump(new_item_dict, fp)

def get_max_val_idx(d):
	v = list(d.values())
	k = list(d.keys())
	return k[v.index(max(v))], max(v)


if __name__ == "__main__":
	main()