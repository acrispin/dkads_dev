define(['text!templates/process/storageOrder.html'],
function (Template) {

        var StorageOrderView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(Template),
            render: function () {
                var html = this.template({ ListData: [] });
                this.$el.html(html);
            }
        });

        return StorageOrderView;
    }
);