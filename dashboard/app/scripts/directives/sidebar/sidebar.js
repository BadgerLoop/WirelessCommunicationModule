'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */

angular.module('sbAdminApp')
  .directive('sidebar',['$location',function($riffle) {
    return {
      templateUrl:'scripts/directives/sidebar/sidebar.html',
      restrict: 'E',
      replace: true,
      scope: {
      },
      controller:function($scope,$riffle){
        $scope.selectedMenu = 'dashboard';
        $scope.collapseVar = 0;
        $scope.multiCollapseVar = 0;
        
        $scope.check = function(x){
          
          if(x==$scope.collapseVar)
            $scope.collapseVar = 0;
          else
            $scope.collapseVar = x;
        };
        
        $scope.multiCheck = function(y){
          
          if(y==$scope.multiCollapseVar)
            $scope.multiCollapseVar = 0;
          else
            $scope.multiCollapseVar = y;
        };
        $scope.start = function(){
          console.log('Starting the run')
          $riffle.publish('cmd', "400#1803")
          console.log('Sent CAN message 400#1803')
        };
        $scope.stop = function(){
          console.log('stopping pod')
          for (var i = 0; i<20; i++){
            $riffle.publish('cmd', "004#1805")
            console.log('Sent CAN message 004#1805')
          } 
        };
        $scope.e_stop = function(y){
          console.log('emergency stopping pod')
            for (var i = 0; i<20; i++){
              $riffle.publish('cmd', "004#1806")
              console.log('Sent CAN message 004#1806')
          } 
        };
      }
    }
  }]);
