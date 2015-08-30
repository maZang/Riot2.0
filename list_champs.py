import json

with open('champ_dict.json', 'r') as df:
	champ_dict = json.load(df)
champ_dict_list = []
for key in champ_dict:
	champ_dict_list.append(key)
print(champ_dict_list)