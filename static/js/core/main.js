require.config({
    baseUrl: main_globals.virtualPath,
    paths: {
        text: 'static/js/libs/text',        
        templates: 'static/templates',
        notify: 'static/js/libs/notify.min',
        ajaxcore: 'static/js/utils/ajaxcore',
        handlebarsHelper: 'static/js/utils/handlebars.helpers',
        utils: 'static/js/utils/main',
        data: 'static/js/core/data',
        app: 'static/js/core/app',
        router: 'static/js/core/router',
        views: 'static/js/core/views',
        validator: 'static/js/libs/validator.min',
        alertify: 'static/js/libs/alertify.min'
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
