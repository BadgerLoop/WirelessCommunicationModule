var app = angular.module('logger', ['ngRoute', 'ngResource', 'ngRiffle']);

app.config(function($routeProvider) {
	'use strict';

	$routeProvider
	.when('/', {
		templateUrl: 'pages/log.html',
		controller: 'LogController'
	})
	.otherwise({
		redirectTo: '/'
	});
	// .config(function($riffleProvider) {
  	//   $riffleProvider.setDomain("xs.node");
  	//   $riffleProvider.setFabric("ws://badgerloop-nuc-1:9000");
  	//   $riffleProvider.setFabricLocal(); FOR LOCAL NODE USE
  	// })
  	// .run(function($riffle){
  	//       //$riffle.setToken("APP_TOKEN");
  	//       $riffle.join();
  	// });
});

app.controller('LogController', function($scope, $http, msgService, socket) {
	
	$scope.messages = msgService.query();
	$scope.saved = [];

	socket.on('new-entry', function() {
		$scope.messages = msgService.query();
	});

	$scope.remove = function(msg) {
		var index = $scope.saved.indexOf(msg);
		$scope.saved.splice(index, 1);
	};

	$scope.add = function(msg) {
		if($scope.saved.indexOf(msg) == -1) {
			$scope.saved.push(msg);
		}
	};
}); 

app.factory('msgService', function($resource) {
	return $resource('logger/messages', {});
});

app.factory('socket', function($rootScope) {
	var socket = io.connect();

	return {
		on: function(eventName, callback) {
			socket.on(eventName, callback);
		},
		emit: function(eventName, data) {
			socket.emit(eventName, data);
		}
	}
});
