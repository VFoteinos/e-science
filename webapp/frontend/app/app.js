// Ember application for e-science.
window.App = Ember.Application.create({
    VERSION : '0.2',
    // Basic logging
    LOG_TRANSITIONS : true,
    // LOG_TRANSITIONS_INTERNAL: true,
    // LOG_ACTIVE_GENERATION : true,
    // LOG_VIEW_LOOKUPS : true,
    // LOG_BINDINGS : true,
    // LOG_RESOLVER: true,
    rootElement : 'body',
    
    ready : function() {
        var that = this;
        var store = this.__container__.lookup('store:main');
        var vrecreatecontroller = this.__container__.lookup('controller:vreserverCreate');
        var clustercreatecontroller = this.__container__.lookup('controller:clusterCreate');
        store.fetch('setting', {}).then(function(data) {
            var settings = data.get('content');
            that.set('AppSettings',settings);
            Ember.set(vrecreatecontroller, 'AppSettings', settings);
            Ember.set(clustercreatecontroller, 'AppSettings', settings);
        }, function(reason) {
            console.log(reason);
        }); 
    },
}); 

App.attr = DS.attr;

// Global variable for e-science token
// for authorization purposes
var escience_token;
App.set('escience_token', "null");