//IFFE
(function(){



	//creating app
	var app = angular.module("champPuller", []);


	//MainController
	var MainController = function($scope, $http){

		var champDict = {"Pantheon": 0, "Vladimir": 85, "Malzahar": 1, "Zed": 2, "Leblanc": 3, "Tryndamere": 62, "Swain": 5, "Nami": 6, "Irelia": 7, 
		"Leona": 8, "Shen": 9, "Sona": 10, "Jax": 11, "Nocturne": 12, "MissFortune": 14, "Graves": 16, "Khazix": 36, "Chogath": 17, "Nautilus": 18, 
		"Trundle": 19, "Brand": 20, "Alistar": 101, "Maokai": 21, "MonkeyKing": 22, "TwistedFate": 23, "Sivir": 24, "Warwick": 25, "Azir": 125, "Elise": 26, 
		"Gragas": 27, "Lux": 29, "Darius": 30, "Quinn": 31, "DrMundo": 32, "Shyvana": 33, "Talon": 34, "Ryze": 35, "Draven": 73, "Renekton": 37, "Karma": 38, 
		"Jayce": 39, "Yasuo": 41, "Rengar": 109, "Katarina": 43, "Annie": 45, "Varus": 47, "Hecarim": 48, "Kalista": 49, "Twitch": 50, "Malphite": 64, 
		"Zyra": 63, "RekSai": 53, "Syndra": 70, "Evelynn": 56, "Lulu": 57, "Skarner": 58, "Kayle": 60, "Sion": 61, "Mordekaiser": 4, "Diana": 51, 
		"Sejuani": 15, "Urgot": 65, "Ekko": 66, "FiddleSticks": 67, "Amumu": 68, "Nunu": 69, "Teemo": 40, "Lissandra": 71, "Blitzcrank": 72, "Fiora": 93, 
		"Kennen": 74, "Shaco": 75, "Zilean": 121, "Ziggs": 76, "Yorick": 77, "Caitlyn": 90, "Thresh": 79, "XinZhao": 80, "Morgana": 81, "Heimerdinger": 82, 
		"Volibear": 83, "Poppy": 84, "Ahri": 55, "Vayne": 86, "Aatrox": 52, "Lucian": 88, "Braum": 89, "Kassadin": 13, "Ashe": 91, "Anivia": 92, "Rammus": 78, 
		"Olaf": 116, "Jinx": 105, "Bard": 94, "Riven": 95, "Viktor": 96, "LeeSin": 97, "Velkoz": 98, "Vi": 99, "TahmKench": 100, "Xerath": 46, "Karthus": 102, 
		"Tristana": 103, "MasterYi": 104, "JarvanIV": 28, "Udyr": 106, "Nidalee": 107, "Nasus": 108, "Gnar": 42, "Ezreal": 110, "KogMaw": 111, "Zac": 112, 
		"Garen": 113, "Galio": 114, "Singed": 115, "Taric": 44, "Veigar": 117, "Fizz": 118, "Rumble": 119, "Soraka": 120, "Corki": 87, "Gangplank": 54, 
		"Orianna": 59, "Cassiopeia": 123, "Akali": 124, "Janna": 122};

		var itemDict = {"Nocturne": ["3153", "3143", "3930", "3074", "3931", "3652", "3117", "3142", "3924", "1329"], 
		"Twitch": ["3153", "3006", "1055", "3031", "3142", "1304", "3652", "1037", "3035", "3087"], 
		"Ryze": ["3027", "3040", "3070", "3020", "1058", "3110", "1314", "1001", "1052", "1026"], 
		"Lulu": ["2049", "3117", "3092", "1329", "3089", "1056", "1052", "3431", "1058", "3157"], 
		"Heimerdinger": ["3157", "1056", "3020", "3089", "1058", "1052", "1314", "1026", "3430", "3116"], 
		"Amumu": ["3725", "3047", "3110", "3151", "3001", "3800", "3742", "3111", "3709", "3116"], 
		"Ahri": ["3285", "1056", "3020", "1314", "3089", "3431", "1058", "3157", "1052", "3434"], 
		"Tristana": ["3031", "1055", "3006", "3046", "1304", "3072", "1053", "3035", "3150", "3087"], "Shen": ["3068", "3065", "1054", "3047", "3742", "3075", "3111", "1028", "3143", "2049"], "XinZhao": ["3153", "3930", "3071", "3117", "3065", "3924", "3652", "3111", "3143", "3707"], "Udyr": ["3078", "3930", "3110", "3153", "1324", "3111", "3742", "3933", "3065", "3047"], "Maokai": ["3027", "3065", "3110", "1056", "3800", "3047", "3111", "3725", "3742", "3211"], "Annie": ["3027", "1056", "3020", "3285", "3089", "1058", "1052", "1314", "2049", "3157"], "Anivia": ["3027", "3020", "1056", "3040", "1314", "3089", "1058", "3151", "3070", "1052"], "Warwick": ["3153", "3091", "3065", "3117", "3933", "3931", "3930", "1329", "3652", "3110"], "Ziggs": ["1056", "3020", "3285", "3174", "3089", "1058", "1314", "1052", "1026", "3430"], "Katarina": ["3285", "3020", "3157", "1314", "3089", "3829", "1052", "1058", "1026", "3001"], "Diana": ["3020", "3157", "1314", "3089", "1056", "3115", "3724", "3100", "3001", "3285"], "Jinx": ["3031", "1055", "3006", "3087", "3072", "3046", "1304", "3035", "1053", "3150"], "Kennen": ["3157", "3020", "1055", "3829", "3089", "1052", "1058", "1314", "3116", "1026"], "Vladimir": ["3152", "3157", "3020", "3116", "3065", "1052", "3089", "1054", "1314", "1058"], "Xerath": ["1056", "3020", "3285", "3089", "3174", "1058", "1314", "3431", "1052", "3434"], "Kassadin": ["3027", "3020", "2041", "3285", "1314", "1058", "3157", "1052", "1026", "3100"], "Sivir": ["3031", "1055", "3006", "3087", "3072", "1304", "3046", "3150", "1053", "3035"], "Zyra": ["2049", "3020", "3151", "3092", "1314", "3116", "1052", "1058", "3089", "3157"], "MissFortune": ["3031", "3006", "1055", "3087", "3072", "1304", "3150", "1053", "3035", "3046"], "Rammus": ["3075", "3725", "1329", "3742", "3143", "3068", "1029", "1031", "1011", "3709"], "Talon": ["3074", "3142", "3035", "2041", "3117", "3924", "3071", "1329", "1037", "1036"], "Thresh": ["2049", "3117", "3069", "1329", "3401", "3190", "3742", "2045", "3110", "3143"], "Swain": ["3027", "1056", "3020", "3157", "1058", "1314", "1052", "1001", "3151", "3434"], "JarvanIV": ["3074", "3071", "3143", "3035", "3707", "3111", "3924", "3742", "1324", "3117"], "DrMundo": ["3065", "3068", "3083", "3047", "3742", "1054", "3075", "1011", "3911", "3111"], "Galio": ["3174", "3111", "1056", "3001", "1324", "3065", "3157", "3829", "3744", "2049"], "Malzahar": ["3027", "1056", "3020", "3089", "3151", "1314", "1058", "3285", "1052", "3434"], "Vi": ["3707", "3078", "3071", "3047", "3143", "3111", "3742", "3652", "1319", "1028"], "Urgot": ["3071", "3042", "1055", "3004", "3047", "3035", "3110", "3044", "1001", "2003"], "Janna": ["2049", "3069", "3117", "3840", "1329", "2045", "3190", "1052", "3504", "3041"], "Leona": ["2049", "3401", "3111", "3068", "3742", "3911", "3117", "3097", "2045", "1028"], "Singed": ["3027", "3116", "3070", "2041", "3040", "3111", "3151", "3431", "1324", "3075"], "Chogath": ["3027", "1056", "3110", "3111", "3089", "1324", "3829", "3742", "1058", "3143"], "Poppy": ["3078", "2041", "3144", "3924", "3153", "3047", "3074", "3143", "1001", "3057"], "Tryndamere": ["3153", "3087", "3031", "3924", "3006", "1304", "1055", "1037", "1038", "3035"], "Rengar": ["3074", "3142", "3707", "3035", "3117", "3924", "1329", "1037", "3723", "1036"], "Sion": ["3110", "3742", "3047", "3065", "3071", "3083", "3111", "1054", "3074", "3924"], "Nami": ["2049", "3117", "3092", "1329", "3744", "3840", "2045", "3174", "1052", "3303"], "Shyvana": ["3153", "3065", "3143", "3930", "3068", "3047", "3931", "3742", "3074", "3111"], "Gragas": ["3725", "3065", "3027", "3020", "3709", "1056", "3111", "3742", "1001", "3829"], "Sona": ["2049", "3092", "3158", "3100", "3174", "3303", "3098", "3504", "2045", "1052"], "Karma": ["2049", "3020", "1052", "3431", "3092", "3285", "3151", "1058", "1314", "3089"], "Nautilus": ["2049", "3401", "3117", "3110", "3742", "3111", "3027", "3800", "1011", "1028"], "MasterYi": ["3153", "3006", "3031", "1304", "3930", "3087", "3652", "3142", "3931", "3924"], "Yorick": ["3042", "2041", "3004", "3065", "3111", "3025", "3924", "1324", "3110", "3078"], "Renekton": ["3074", "3071", "3111", "3065", "3924", "3143", "3742", "3075", "3068", "1054"], "Caitlyn": ["3031", "3006", "1055", "3046", "3087", "3072", "1053", "3035", "1304", "3150"], "Kayle": ["3115", "3085", "3006", "1056", "3020", "3930", "1304", "3933", "3089", "1052"], "Elise": ["3020", "3151", "3708", "1314", "3116", "3829", "3001", "3724", "3136", "1052"], "TwistedFate": ["3100", "3285", "1056", "3020", "3089", "3157", "1314", "1058", "3431", "1052"], "Sejuani": ["3725", "3110", "3117", "3143", "3742", "3083", "1329", "3709", "1028", "3102"], "Zac": ["3065", "3709", "3143", "3083", "3725", "1028", "1011", "3117", "3111", "3742"], "Braum": ["2049", "3401", "3117", "3911", "3742", "1028", "3097", "1329", "3068", "2045"], "Shaco": ["3074", "3707", "3087", "3006", "3031", "1304", "1037", "3117", "1036", "1038"], "Viktor": ["3198", "1056", "3020", "3089", "3285", "1314", "1058", "1052", "3197", "1026"], "Azir": ["1056", "3020", "3089", "1314", "1058", "3174", "1052", "3115", "1026", "3157"], "Volibear": ["3065", "3742", "3083", "3709", "3143", "3075", "3717", "3111", "1011", "3068"], "Lux": ["3020", "1056", "3285", "3089", "3174", "1058", "1052", "1314", "1026", "3431"], "Irelia": ["3078", "2041", "3153", "3065", "3047", "3143", "3111", "3924", "3211", "1319"], "Gnar": ["1055", "3153", "3068", "3111", "3143", "3065", "3071", "3652", "3742", "1324"], "Skarner": ["3709", "3078", "3025", "3742", "3117", "3110", "3800", "3111", "1329", "1028"], "Quinn": ["3031", "1055", "3006", "3087", "3072", "1304", "3150", "3153", "1038", "1037"], "Ashe": ["3031", "3006", "1055", "3046", "3072", "3087", "1053", "3150", "1304", "3652"], "Varus": ["3031", "3006", "1055", "3072", "3035", "3087", "3085", "1304", "1053", "3150"], "Trundle": ["3153", "3065", "3924", "3111", "3742", "3047", "3143", "3074", "3211", "1324"], "Jayce": ["3042", "3158", "3035", "3004", "1055", "3071", "1334", "3031", "1038", "3044"], "Rumble": ["3151", "3020", "3157", "1314", "3116", "1054", "1052", "1026", "3829", "1058"], "Olaf": ["3074", "3065", "3153", "3924", "3047", "3742", "1319", "3110", "3143", "3111"], "LeeSin": ["3707", "3074", "2049", "3071", "3143", "3117", "1329", "3035", "3924", "3742"], "Teemo": ["3151", "3115", "3020", "1056", "3089", "3085", "1314", "1052", "1026", "1058"], "Cassiopeia": ["1056", "3040", "3020", "3285", "3070", "1314", "1058", "3089", "3116", "1052"], "Fizz": ["3100", "3157", "1056", "3020", "3089", "1314", "1058", "1052", "3153", "3078"], "Veigar": ["3089", "1056", "3020", "1314", "3135", "1058", "1026", "3157", "1052", "3285"], "Nidalee": ["3020", "3724", "3089", "3285", "1056", "1058", "1314", "1052", "3027", "3157"], "Blitzcrank": ["2049", "3117", "3069", "1329", "3025", "3110", "2045", "3829", "3401", "3800"], "Nasus": ["3065", "3110", "3078", "2041", "3111", "3025", "3924", "3057", "1324", "3143"], "Akali": ["3146", "3020", "3100", "3157", "3116", "1314", "3089", "1052", "1058", "1001"], "Brand": ["3151", "3020", "1056", "3285", "1314", "3116", "3089", "1058", "1052", "3434"], "Ekko": ["3285", "3100", "3020", "2041", "1314", "3157", "1058", "3089", "3431", "1052"], "Lucian": ["3031", "1055", "3006", "3087", "3072", "1304", "3035", "1053", "3150", "1037"], "Graves": ["3031", "1055", "3006", "3087", "3072", "1304", "3035", "3150", "1053", "3046"], "Lissandra": ["3157", "3027", "1056", "3020", "1314", "3089", "1058", "1052", "1026", "3434"], "Corki": ["3078", "1055", "3020", "3031", "3153", "1314", "3072", "1037", "3035", "1038"], "Vayne": ["3153", "3006", "1055", "3652", "3046", "1304", "3031", "3087", "3035", "1037"], "Garen": ["3068", "3071", "3065", "1054", "3009", "3742", "3083", "3143", "3075", "1011"], "Ezreal": ["1055", "3078", "3158", "3042", "3035", "1334", "3004", "3153", "3025", "3031"], "Draven": ["3031", "3006", "1055", "3072", "3035", "3087", "1304", "3046", "3150", "1053"], "Nunu": ["3721", "3117", "3110", "3065", "2049", "3725", "1329", "3143", "3027", "3742"], "Evelynn": ["3708", "3117", "3707", "3143", "1329", "3153", "3116", "3146", "3285", "1052"], "Soraka": ["2049", "3069", "3158", "3504", "3117", "1052", "3840", "1334", "2045", "3089"], "Zed": ["3153", "3142", "3035", "3924", "3071", "3111", "3072", "3134", "1324", "1036"], "Pantheon": ["3071", "3074", "2041", "3035", "3924", "3707", "3047", "3117", "3156", "1037"], "Kalista": ["3085", "3006", "1055", "3153", "3072", "1304", "3652", "3035", "1053", "1042"], "Khazix": ["3074", "3707", "3035", "3071", "3723", "3117", "1329", "1036", "3924", "1037"], "Bard": ["2049", "3117", "3092", "1329", "3110", "3840", "3069", "3143", "2045", "3829"], "Hecarim": ["3078", "3742", "3065", "2041", "3717", "1324", "3143", "3071", "1329", "3117"], "KogMaw": ["3153", "3078", "1055", "3006", "3285", "1056", "3020", "3040", "3070", "1304"], "Darius": ["3074", "3068", "3924", "3111", "3143", "1054", "1324", "3742", "3071", "3078"], "Fiora": ["3074", "3924", "3006", "3035", "3072", "1304", "1055", "3031", "3142", "1037"], "RekSai": ["3707", "3074", "3111", "3143", "3709", "3065", "3742", "1011", "1324", "3071"], "MonkeyKing": ["3074", "3071", "3111", "2041", "3924", "3035", "3143", "1324", "3707", "1036"], "Zilean": ["2049", "3158", "3092", "3070", "3040", "3089", "1058", "1052", "1026", "3431"], "FiddleSticks": ["3157", "3020", "3708", "3089", "1058", "1052", "1026", "1314", "1056", "3151"], "Yasuo": ["3087", "3031", "1055", "3006", "3153", "1304", "3924", "1038", "3035", "1037"], "Malphite": ["3068", "3110", "3047", "2041", "3742", "3075", "3001", "3025", "3829", "1319"], "Jax": ["3153", "3078", "3924", "3111", "3652", "3143", "2041", "1324", "3930", "3047"], "Karthus": ["3027", "3040", "3020", "3089", "1056", "3157", "1314", "1058", "3116", "3434"], "Orianna": ["1056", "3020", "3174", "3089", "1058", "1314", "3157", "1052", "1026", "3040"], "Leblanc": ["1056", "3089", "3285", "3020", "1314", "1058", "1052", "3434", "3829", "3157"], "TahmKench": ["2049", "3401", "3009", "3742", "3068", "3065", "1028", "3083", "3911", "1001"], "Aatrox": ["3153", "3074", "3924", "3065", "3652", "3047", "1055", "3143", "3930", "1319"], "Morgana": ["3157", "2049", "3020", "1056", "1058", "1052", "3089", "1314", "3092", "1026"], "Velkoz": ["3020", "1056", "3285", "3089", "3174", "1058", "3434", "1314", "3431", "3157"], "Taric": ["2049", "3401", "3047", "3110", "3742", "3097", "3068", "1029", "3911", "3025"], "Syndra": ["1056", "3020", "3285", "3089", "3174", "1314", "3431", "1052", "3157", "3434"], "Mordekaiser": ["3152", "3020", "3116", "1054", "3089", "3151", "1314", "3157", "1058", "3829"], "Riven": ["3074", "3134", "3035", "3924", "3071", "3158", "3142", "1334", "1036", "3072"], "Alistar": ["2049", "3401", "3117", "1329", "3911", "1028", "3110", "3742", "3800", "2045"]}

		var champPictureReady = function(response){
			$scope.champion = true;
			$scope.errorMsg = "";
			$scope.imgURLchamp = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + $scope.champName + "_0.jpg"; 
			$scope.winRate = champDict[$scope.champName];
		};

		var ifError = function(noChamp){
			$scope.champion = false;
			$scope.errorMsg = "Champion not found!";
		};

		// var itemPictureReady = function(response){
		// 	$scope.imgURLitem="http://ddragon.leagueoflegends.com/cdn/5.2.1/img/item/" + $scope.itemID + ".png";
		// }
	
		$scope.search = function(champName){
			$http.get("http://ddragon.leagueoflegends.com/cdn/5.16.1/img/champion/" + champName + ".png").then(champPictureReady, ifError);

			$scope.imgURLitem = [];
			for(var itemID in itemDict[$scope.champName]){
				console.log(itemID);
				$scope.imgURLitem.push("http://ddragon.leagueoflegends.com/cdn/5.2.1/img/item/" + itemID + ".png");
			}
		};
		
	};


	//assigning controllers to Angular app
	app.controller("MainController" , ["$scope", "$http", MainController]);


}());