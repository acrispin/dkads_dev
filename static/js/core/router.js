define([], function () {

    var AppRouter = Backbone.Router.extend({
        routes: {
            'article': 'showArticle',
            'warehouse': 'showWarehouse',
            'reason': 'showReason',
            'storageOrder': 'showStorageOrder',
            'pickupOrder': 'showPickupOrder',
            'stock': 'showStock',
            'kardex': 'showKardex',
            'user': 'showUser',
            'logout': 'showLogout',
            '*actions': 'defaultAction' // default actions debe ir al ultimo siempre
        }
    });

    var hidden = '#bestTours';    

    function emptyMain() {
        $("#main").html('');
        $("#main").off(); // para evitar que no se repliquen eventos.
        request_ns.showLoading();
        //$('.menu li').removeClass('active');
        //$('.menu li a[href="' + window.location.hash + '"]').parent().addClass('active');
        if ($('.navbar-collapse').hasClass('in')) {
            $('.navbar-collapse').collapse('hide');
        }
    }

    function renderView(view) {
        view.render();
        request_ns.hideLoading();
        $("html, body").scrollTop('0');
    }

    Backbone.View.prototype.close = function () {
        this.$el.empty().off();
        this.stopListening();
        if (this.onClose) {
            this.onClose();
        }
    }

    function AppView() {
        this.showView = function (view) {
            if (this.currentView) {
                this.currentView.close();
            }
            this.currentView = view;
            this.currentView.render();
            request_ns.hideLoading();
            $("html, body").scrollTop('0');
        };        
    }

    var initialize = function () {

        var app_router = new AppRouter;
        var app_view = new AppView;
       
        // home
        app_router.on('route:defaultAction', function (actions) {
            try {
                emptyMain();
                require(['views/main/home'], function (HomeView) {
                    var homeView = new HomeView();
                    renderView(homeView);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });

        // articulos
        app_router.on('route:showArticle', function () {
            try {
                emptyMain();
                require(['views/entities/article'], function (ArticleView) {
                    var _view = new ArticleView();
                    renderView(_view);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });

        // almacenes
        app_router.on('route:showWarehouse', function () {
            try {
                emptyMain();
                require(['views/entities/warehouse'], function (WarehouseView) {
                    var _view = new WarehouseView();
                    renderView(_view);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });

        // motivos
        app_router.on('route:showReason', function () {
            try {
                emptyMain();
                require(['views/entities/reason'], function (ReasonView) {
                    var _view = new ReasonView();
                    renderView(_view);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });
        
        // ingresos
        app_router.on('route:showStorageOrder', function () {
            try {
                emptyMain();
                require(['views/process/storageOrder'], function (StorageOrderView) {
                    var _view = new StorageOrderView();
                    renderView(_view);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });

        // salidas
        app_router.on('route:showPickupOrder', function () {
            try {
                emptyMain();
                require(['views/process/pickupOrder'], function (PickupOrderView) {
                    var _view = new PickupOrderView();
                    renderView(_view);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });

        // stock
        app_router.on('route:showStock', function () {
            try {
                emptyMain();
                require(['views/reports/stock'], function (StockView) {
                    var _view = new StockView();
                    renderView(_view);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });

        // kardex
        app_router.on('route:showKardex', function () {
            try {
                emptyMain();
                require(['views/reports/kardex'], function (KardexView) {
                    var _view = new KardexView();
                    renderView(_view);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });

        // usuarios
        app_router.on('route:showUser', function () {
            try {
                emptyMain();
                require(['views/security/user'], function (UserView) {
                    var _view = new UserView();
                    renderView(_view);
                }, function (err) {
                    var failedId = err.requireModules && err.requireModules[0];
                    console.log(err.requireType);
                    console.log('modules: ' + err.requireModules);
                    requirejs.undef(failedId);
                    request_ns.clearLoading();
                    if (main_globals.flagDevelop) {
                        alert(err.requireType + "-" + failedId);
                    }
                    main_ns.renderTemplate("#main", "#error_template", []);
                });
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });

        // salir de session
        app_router.on('route:showLogout', function () {
            try {
                console.log("implementar salir de session");
            } catch (e) {
                console.log(e);
                main_ns.msgError("Sucedió un error inesperado.");
                request_ns.clearLoading();
                if (main_globals.flagDevelop) {
                    alert(e);
                }
            }
        });
        
        Backbone.history.start();
    };

    return {
        initialize: initialize
    };

});
