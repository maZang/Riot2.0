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
		var champDict = {};

		$http.get("champ_dict.json").success(function(data){
			champDict = data;
		});

		$('.winRate').html(champDict['Aatrox']);
	};



	//assigning controllers to Angular app
	app.controller("PictureController" , ["$scope", "$http", PictureController]);
	app.controller("TableController", ["$scope", "$http", TableController]);




}());