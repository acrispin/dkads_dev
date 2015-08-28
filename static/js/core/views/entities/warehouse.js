define(['text!templates/entities/warehouse.html'],
function (Template) {

        var WarehouseView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(Template),
            render: function () {
                var html = this.template({ ListData: [] });
                this.$el.html(html);
            }
        });

        return WarehouseView;
    }
);