define(['text!templates/process/pickupOrder.html'],
function (Template) {

        var PickupOrderView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(Template),
            render: function () {
                var html = this.template({ ListData: [] });
                this.$el.html(html);
            }
        });

        return PickupOrderView;
    }
);