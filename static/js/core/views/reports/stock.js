define(['text!templates/reports/stock.html'],
function (Template) {

        var StockView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(Template),
            render: function () {
                var html = this.template({ ListData: [] });
                this.$el.html(html);
            }
        });

        return StockView;
    }
);