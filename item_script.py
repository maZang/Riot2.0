import json 

def main():
	new_item_dict = {}
	with open('item_dict.json', 'r') as df:
		pop_items= json.load(df)
	for champ in pop_items:
		new_item_list = []
		item_dict = pop_items[champ]	
		for item in range(0, 10):
			item_idx = get_max_val_idx(item_dict)
			del item_dict[item_idx]
			new_item_list.append(item_idx)
		new_item_dict[champ] = new_item_list
	with open('pop_item_dict.json', 'w') as fp:
		json.dump(new_item_dict, fp)

def get_max_val_idx(d):
	v = list(d.values())
	k = list(d.keys())
	return k[v.index(max(v))]


if __name__ == "__main__":
	main()