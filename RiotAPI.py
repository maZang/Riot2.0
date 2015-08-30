import requests
import RiotConsts as Consts 

class RiotAPI(object):

	def __init__(self, api_key, region=Consts.REGIONS['north_america']):
		self.api_key = api_key
		self.region = region

	def _request(self, api_url, static, params={}):
		args = {'api_key': self.api_key}
		for key, value in params.items():
			if key not in args:
				args[key] = value
		while True:
			if not static:
				response = requests.get(Consts.URL['base'].format(proxy=self.region,region=self.region,url=api_url), params=args)
			else:
				response = requests.get(Consts.URL['static_base'].format(proxy='global',region=self.region,url=api_url), params=args)
			#print(response.url)
			if response.status_code == Consts.RATE_ERROR_CODE:
				print("Rate limit exceeded... Currently waiting")
				continue
			if response.status_code == Consts.NOT_FOUND:
				return False
			if response.status_code != Consts.SUCCESS_CODE:
				print("Unknown Error with status code " + str(response.status_code))
				continue
			break
		return response.json()

	def get_summoner_by_name(self, name):
		api_url = Consts.URL['summoner_by_name'].format(version=Consts.API_VERSION['summoner'], names=name)
		return self._request(api_url, False)

	def get_match_info(self, idnum, params={}):
		api_url = Consts.URL['matchhistory'].format(version=Consts.API_VERSION['match'], matchid = idnum)
		return self._request(api_url, False, params)

	def get_item_by_id(self, idnum, params={}):
		api_url = Consts.URL['static_data_itemid'].format(version=Consts.API_VERSION['static_data'], itemid = idnum)
		return self._request(api_url, True, params)

	def get_champ_by_id(self, idnum, params={}):
		api_url = Consts.URL['static_data_champid'].format(version=Consts.API_VERSION['static_data'], champid = idnum)
		return self._request(api_url, True, params)

	def get_rune_by_id(self, idnum, params={}):
		api_url = Consts.URL['static_data_runeid'].format(version=Consts.API_VERSION['static_data'], runeid = idnum)
		return self._request(api_url, True, params)

	def get_mastery_by_id(self, idnum, params={}):
		api_url = Consts.URL['static_data_masteryid'].format(version=Consts.API_VERSION['static_data'], masteryid = idnum)
		return self._request(api_url, True, params)

	def get_all_champs(self, params={}):
		api_url = Consts.URL['static_data_allchamps'].format(version=Consts.API_VERSION['static_data'])
		return self._request(api_url, True, params)