angular.module('demo', [])
.controller('Dice', function($scope, $http) {

//    $scope.sides = "6"
//    $scope.quantity = "1"

    $scope.rollDice = function() {

        var config = {
            params: {
                sides: $scope.sides,
                quantity: $scope.quantity
            }
        }

        $http.get('http://localhost:5000/roll', config).
            then(function(response) {
                $scope.response = response.data;
            });
    };
    $scope.rollDice()
});