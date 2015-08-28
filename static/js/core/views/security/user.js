define(['text!templates/security/user.html'],
function (Template) {

        var UserView = Backbone.View.extend({
            el: $("#main"),
            template: Handlebars.compile(Template),
            render: function () {
                var html = this.template({ ListData: [] });
                this.$el.html(html);
            }
        });

        return UserView;
    }
);