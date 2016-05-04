angular
    .module('VesaliusApp', ['ngRoute', 'ui.bootstrap'])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '../static/vesalius5.html',
                controller: 'VesaliusController'
            })
            .otherwise({ redirectTo: '/' });
    }])
    .factory('windowAlert', [
        '$window',
        function($window) {
            return $window.alert;
        }
    ])
    .controller('VesaliusController', [
        '$scope',
        '$http',
        'windowAlert',
        function($scope, $http, windowAlert) {


            $scope.state = {};
            $scope.RETRIEVE_DEFAULT_ZONEGROUP = '76';
            $scope.state.retrieveZonegroup = $scope.RETRIEVE_DEFAULT_ZONEGROUP;
            $scope.zonegroup = "76";
            $scope.selectedzonegroup = "88";

            $scope.state.descriptionList = [];
            $scope.state.mediaList = [];


            $scope.namespace = '/vesalius5'; // change to an empty string to use the global namespace

            // the socket.io documentation recommends sending an explicit package upon connection
            // this is specially important when using the global namespace
            var socket = io.connect('http://' + document.domain + ':' + location.port + $scope.namespace);

            // event handler for new connections
            socket.on('connect', function() {
                console.log('Connected');
                socket.emit('my event', {data: 'I\'m connected!'});
            });


            // event handler for server sent data
            socket.on('my response', function(msg) {
                console.log(msg.zonegroup);
    
                //$( "#zonegroup" ).val(msg.zonegroup).trigger("input");
                $scope.zonegroup = msg.zonegroup;
                $scope.setAndRetrieveMetadataByZonegroup($scope.zonegroup);
            });
            
            
            $scope.sendBackToServer =  function(zonegroup){
                if ($scope.selectedzonegroup != zonegroup){
                    socket.emit('zonegroup', zonegroup);
                }
            }

            $scope.retrieveMetadataByZonegroup = function(zonegroup) {
                $http
                    .get('/metadataByZonegroup/' + zonegroup)
                    .success(function(data, status, headers, config) {
                        if (data.success) {
                            $scope.state.descriptionList = data.descriptionList;
                  
                            $scope.state.mediaList = data.mediaList;
                        } else {
                            windowAlert('Retrieval failed - '+data.descipitonList + 'and ' + data.mediaList);
                        }
                    })
                    .error(function(data, status, headers, config) {
                        windowAlert("Retrieval failed - " + data.descipitonList + 'and ' + data.mediaList);
                    });
            };

            $scope.setAndRetrieveMetadataByZonegroup = function(zonegroup) {
                if (!zonegroup || 0 === zonegroup.length ){
                    zonegroup = $scope.RETRIEVE_DEFAULT_ZONEGROUP;
                }
                

                if ($scope.selectedzonegroup != zonegroup){
                    $scope.state.retrieveZonegroup = zonegroup;
                    $scope.retrieveMetadataByZonegroup($scope.state.retrieveZonegroup);

                    $scope.changeOpacityById($scope.selectedzonegroup, '.2');
                    $scope.changeOpacityById(zonegroup, '.8');
                    $scope.zonegroup = zonegroup;
                    $scope.selectedzonegroup = zonegroup;
                }
            };


            $scope.changeOpacityById = function(id, op){

                var organs = document.getElementsByClassName(id);
                //console.log(organs);

                for (i = 0; i < organs.length; i++) {
                    organs[i].style.opacity=op;
                }
            }

        }
    ])
    .directive('vesaliusSvg', function()  {
        return{
            restrict: 'AE',
            replace: true,
            templateUrl: '../static/svg/output-angular.svg',
            link: function(scope, element, attrs) {
                var target = document.getElementsByTagName('path');
                for (var i = 0; i < target.length; i++) {
                    
                    $(target[i]).on('click', function(){
                        var id = $(this).attr('class');
                        scope.sendBackToServer(id);
                        scope.setAndRetrieveMetadataByZonegroup(id);
                       
                    });
                    $(target[i]).on('mouseover', function(){
                        var id = $(this).attr('class');
                        if(id != scope.selectedzonegroup){
                            scope.changeOpacityById(id, '.6'); 
                        }
                    });
                     $(target[i]).on('mouseout', function(){
                        var id = $(this).attr('class');
                        if(id != scope.selectedzonegroup){
                            scope.changeOpacityById(id, '.2'); 
                        }
                    });
                }
                
           }
        }
    })
  
    .filter('unsafe', function($sce) {
        return function(val) {
            return $sce.trustAsHtml(val);
        }
    });
    
    
