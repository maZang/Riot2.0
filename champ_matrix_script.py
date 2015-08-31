#used to make a CHAMP_TO_MATRIX for FetchData.py (converting from champion to index)
import requests
import RiotConsts as Consts 
from RiotAPI import RiotAPI
import json

api = RiotAPI('be8ccf5f-5d08-453f-84f2-ec89ddd7cea2')
champs = api.get_all_champs()
champ_dict = {}
index = 0
for champ in champs['data'].keys():
	champ_dict[champ] = index
	index += 1
with open('champ_dict.json', 'w') as fp:
	json.dump(champ_dict, fp)