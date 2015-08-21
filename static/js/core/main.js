require.config({
    baseUrl: main_globals.virtualPath,
    paths: {
        text: 'Static/js/libs/text',        
        templates: 'Static/templates',
        notify: 'Static/js/libs/notify.min',
        ajaxcore: 'Static/js/utils/ajaxcore',
        handlebarsHelper: 'Static/js/utils/handlebars.helpers',
        utils: 'Static/js/utils/utils',
        data: 'Static/js/core/data',
        app: 'Static/js/core/app',
        router: 'Static/js/core/router',
        views: 'Static/js/core/views',
        validator: 'Static/js/libs/validator.min',
        alertify: 'Static/js/libs/alertify.min'
    },
    shim: {
        "notify": { "deps": [] },
        "utils": { "deps": ['notify', 'validator'] },
        "handlebarsHelper": { "deps": ['utils'] },
        "ajaxcore": { "deps": ['utils'] }
    },
    //waitSeconds : 15,
    urlArgs: "v=" + (main_globals.flagDevelop ? (new Date()).getTime() : main_globals.sysVersion)
});


require(['app', 'utils', 'handlebarsHelper', 'ajaxcore', 'validator', 'alertify'],
    function (App) {   
        App.initialize();
});
