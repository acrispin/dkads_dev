define(['text!templates/reports/kardex.html'],
function (Template) {

        var KardexView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(Template),
            render: function () {
                var html = this.template({ ListData: [] });
                this.$el.html(html);
            }
        });

        return KardexView;
    }
);