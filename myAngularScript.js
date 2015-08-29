//IFFE
(function(){



	//creating app
	var app = angular.module("champPuller", []);



	//PictureController
	var PictureController = function($scope, $http){

	var pictureReady = function(response){
		$scope.champion = true;
		$scope.errorMsg = "";
		$scope.imgURL = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + $scope.champName + "_0.jpg"; 
	}

	var ifError = function(noChamp){
		$scope.champion = false;
		$scope.errorMsg = "Champion not found!";
	}
	
	$scope.search = function(champName){
		$http.get("http://ddragon.leagueoflegends.com/cdn/5.16.1/img/champion/" + champName + ".png").then(pictureReady, ifError);
	}
	};



	//TableController
	var TableController = function($scope, $http){

		//champDict assignment
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

		$scope.winRate = champDict[$scope.champName];
	
	};



	//assigning controllers to Angular app
	app.controller("PictureController" , ["$scope", "$http", PictureController]);
	app.controller("TableController", ["$scope", "$http", TableController]);




}());