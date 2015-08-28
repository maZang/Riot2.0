(function(){

var app = angular.module("champPuller", []);

var PictureController = function($scope, $http){



var ifError = function(noChamp){
	$scope.error = "Champion not found!";
}

};

$scope.search = function{
	$http.get("http://ddragon.leagueoflegends.com/cdn/5.2.1/img/champion/" + $scope.champName + ".png").then(avatarReady,ifError);
}

app.controller("PictureController" , PictureController);

}());