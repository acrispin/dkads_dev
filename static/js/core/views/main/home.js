define(['text!templates/main/home.html'],
function (homeTemplate) {

        var HomeView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(homeTemplate),
            render: function () {
                var html = this.template({ ListData: [] });
                this.$el.html(html);
            }
        });

        return HomeView;
    }
);