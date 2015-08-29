(function(){

var app = angular.module("champPuller", []);

var PictureController = function($scope, $http){

var pictureReady = function(response){
	$scope.champion = response.data
}

var ifError = function(noChamp){
	$scope.errorMsg = "Champion not found!";
}
	$scope.champName = "Pony"
};

$scope.search = function{
	$http.get("http://ddragon.leagueoflegends.com/cdn/5.16.1/img/champion/Chogath.png").then(avatarReady,ifError);
}

app.controller("PictureController" , ["$scope", "$http", PictureController]);

}());