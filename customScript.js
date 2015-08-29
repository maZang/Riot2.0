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

app.controller("PictureController" , ["$scope", "$http", PictureController]);

}());