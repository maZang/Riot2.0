(function(){


	var app = angular.module("champPuller", []);

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



	app.controller("PictureController" , ["$scope", "$http", PictureController]);

}());