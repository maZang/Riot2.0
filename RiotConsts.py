#126 champions released during Black Market Brawlers (latest is Tahm Kench)
BLACK_MARKET_CHAMPIONS = 126
#FlatArmorMod, FlatAttackSpeedMod,...rPercentTimeDeadModPerLevel, Range, Kills, Deaths, Assists, CS/min, physical damage, magic damage, true damage, 
#damage taken, team jgl, enemy jgl, GoldEarned/min, Offense, Defense, Utility, spell1id, spell2id, 
BLACK_MARKET_FEATURES = 82 #filler

URL = {
	'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
	'static_base': 'https://{proxy}.api.pvp.net/api/lol/static-data/{region}/{url}',
	'summoner_by_name': 'v{version}/summoner/by-name/{names}',
	'matchhistory': 'v{version}/match/{matchid}' ,
	'static_data_itemid': 'v{version}/item/{itemid}',
	'static_data_champid': 'v{version}/champion/{champid}',
	'static_data_runeid': 'v{version}/rune/{runeid}'
	'static_data_masteryid': 'v{version}/mastery/{masteryid}'
}

API_VERSION = {
	'summoner': '1.4',
	'match:': '2.2', 
	'static_data': '1.2'
}

REGIONS = {
	'europe_nordic_and_east': 'eune',
	'europe_west': 'euw',
	'north_america': 'na'
}

STAT_TO_MATRIX = {
	"FlatSpellBlockMod": 1,
    "PercentMPRegenMod": 2,
    "rFlatSpellBlockModPerLevel": 3,
    "rFlatArmorModPerLevel": 4,
    "PercentPhysicalDamageMod": 5,
    "FlatCritChanceMod": 6,
    "PercentSpellBlockMod": 7,
    "rFlatTimeDeadModPerLevel": 8,
    "rFlatMagicDamageModPerLevel": 9,
    "rFlatHPModPerLevel": 10,
    "rPercentMovementSpeedModPerLevel": 11,
    "FlatEXPBonus": 12,
    "FlatMPRegenMod": 13,
    "rFlatHPRegenModPerLevel": 14,
    "FlatBlockMod": 15,
    "PercentEXPBonus": 16,
    "FlatEnergyPoolMod": 17,
    "rFlatEnergyRegenModPerLevel": 18,
    "rFlatGoldPer10Mod": 19,
    "FlatAttackSpeedMod": 20,
    "FlatHPPoolMod": 21,
    "PercentAttackSpeedMod": 22,
    "rFlatDodgeMod": 23,
    "rFlatMPRegenModPerLevel": 24,
    "rPercentTimeDeadMod": 25,
    "FlatEnergyRegenMod": 26,
    "PercentSpellVampMod": 27,
    "FlatCritDamageMod": 28,
    "rFlatMovementSpeedModPerLevel": 29,
    "PercentHPRegenMod": 30,
    "rPercentArmorPenetrationModPerLevel": 31,
    "PercentArmorMod": 32,
    "rFlatMPModPerLevel": 33,
    "rFlatArmorPenetrationMod": 34,
    "PercentBlockMod": 35,
    "PercentMagicDamageMod": 36,
    "FlatMPPoolMod": 37,
    "FlatPhysicalDamageMod": 38,
    "rFlatPhysicalDamageModPerLevel": 39,
    "rFlatTimeDeadMod": 40,
    "FlatHPRegenMod": 41,
    "rFlatCritDamageModPerLevel": 42,
    "rFlatCritChanceModPerLevel": 43,
    "rFlatDodgeModPerLevel": 44, 
    "rPercentMagicPenetrationModPerLevel": 45,
    "PercentLifeStealMod": 46,
    "PercentMovementSpeedMod": 47,
    "FlatArmorMod": 48,
    "rFlatEnergyModPerLevel": 49,
    "rPercentMagicPenetrationMod": 50,
    "rPercentTimeDeadModPerLevel": 51,
    "PercentMPPoolMod": 52,
    "PercentDodgeMod": 53,
    "PercentCritChanceMod": 54,
    "PercentCritDamageMod": 55,
    "rPercentAttackSpeedModPerLevel": 56,
    "rFlatMagicPenetrationMod": 57,
    "PercentHPPoolMod": 58,
    "rPercentArmorPenetrationMod": 59,
    "rFlatMagicPenetrationModPerLevel": 60,
    "rFlatArmorPenetrationModPerLevel": 61,
    "rPercentCooldownModPerLevel": 62,
    "FlatMagicDamageMod": 63,
    "FlatMovementSpeedMod": 64,
    "rPercentCooldownMod": 65
}

VARIABLE_TO_MATRIX = {
	
}