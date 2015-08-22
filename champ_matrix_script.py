#used to make a CHAMP_TO_MATRIX for FetchData.py (converting from champion to index)
import requests
import RiotConsts as Consts 
from RiotAPI import RiotAPI
import json

api = RiotAPI('5692a80d-37e8-476a-8b37-7995789d9bf7')
champs = api.get_all_champs()
champ_dict = {}
index = 0
for champ in champs['data'].keys():
	champ_dict[champs['data'][champ]['name']] = index
	index += 1
with open('champ_dict.json', 'w') as fp:
	json.dump(champ_dict, fp)