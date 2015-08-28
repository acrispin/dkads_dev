define(['text!templates/entities/article.html'],
function (Template) {

        var ArticleView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(Template),
            render: function () {
                var _this = this;
                try{
                    request_ns.post_galo('entities.listArt', {},
                        function (data) {
                            try {
                                var html = _this.template({ ListData: data });
                                _this.$el.html(html);
                            } catch (e) {
                                console.log(e);
                                main_ns.msgError("Sucedió un error inesperado.");
                            }
                        }
                    );
                } catch(e) {
                    console.log(e);
                    main_ns.msgError("Sucedió un error inesperado.");
                }                
            },
            events: {
                'click #btnCreate': 'openPopupCreate'
            },
            openPopupCreate: function (e) {            
                $("#pnlArticulo").modal("show");
            }
        });

        return ArticleView;
    }
);