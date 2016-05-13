var aleph = angular.module('aleph', ['ngRoute', 'ngAnimate', 'ngSanitize', 'ui.bootstrap',
                                     'pdf', 'angulartics', 'angulartics.piwik']);

aleph.config(['$routeProvider', '$locationProvider', '$analyticsProvider',
    function($routeProvider, $locationProvider, $analyticsProvider) {

  $routeProvider.when('/search', {
    templateUrl: 'templates/search.html',
    controller: 'SearchCtrl',
    reloadOnSearch: true,
    loginRequired: false,
    resolve: {
      'data': loadSearch
    }
  });

  $routeProvider.when('/tabular/:document_id/:table_id', {
    templateUrl: 'templates/tabular.html',
    controller: 'TabularCtrl',
    reloadOnSearch: true,
    loginRequired: false,
    resolve: {
      'data': loadTabular,
      'metadata': loadMetadata
    }
  });

  $routeProvider.when('/text/:document_id', {
    templateUrl: 'templates/text.html',
    controller: 'TextCtrl',
    reloadOnSearch: false,
    loginRequired: false,
    resolve: {
      'data': loadText,
      'metadata': loadMetadata,
      'pages': loadPagesQuery
    }
  });

  $routeProvider.when('/entities', {
    templateUrl: 'templates/entity_index.html',
    controller: 'EntitiesIndexCtrl',
    reloadOnSearch: true,
    loginRequired: false,
    resolve: {
      'data': loadEntitiesIndex
    }
  });

  $routeProvider.when('/entities/:entity_id', {
    templateUrl: 'templates/entity_edit.html',
    controller: 'EntitiesEditCtrl',
    reloadOnSearch: true,
    loginRequired: false,
    resolve: {
      'data': loadEntity
    }
  });

  $routeProvider.when('/help/:page', {
    templateUrl: 'templates/help.html',
    controller: 'HelpCtrl',
    reloadOnSearch: false,
    loginRequired: false,
    resolve: {}
  });

  $routeProvider.when('/help', {
    templateUrl: 'templates/help.html',
    controller: 'HelpCtrl',
    reloadOnSearch: false,
    loginRequired: false,
    resolve: {}
  });

  $routeProvider.when('/', {
    templateUrl: 'templates/home.html',
    controller: 'HomeCtrl',
    reloadOnSearch: false,
    loginRequired: false,
    resolve: {
      'data': loadHome
    }
  });

  // $routeProvider.otherwise({
  //   redirectTo: '/',
  //   loginRequired: false
  // });

  $locationProvider.html5Mode(true);
}]);
