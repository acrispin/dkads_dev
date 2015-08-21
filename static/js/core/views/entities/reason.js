define(['text!templates/entities/reason.html'],
function (Template) {

        var ReasonView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(Template),
            render: function () {
                var html = this.template({ ListData: [] });
                this.$el.html(html);
            }
        });

        return ReasonView;
    }
);