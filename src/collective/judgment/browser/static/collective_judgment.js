/*global location: false, window: false, jQuery: false */
(function ($, collective_judgment) {
    "use strict";
    collective_judgment.init_voting_viewlet = function (context) {
        var notyetvoted = context.find("#notyetvoted"),
            alreadyvoted = context.find("#alreadyvoted"),
            delete_votings = context.find("#delete_votings"),
            delete_votings2 = context.find("#delete_votings2");

        if (context.find("#voted").length !== 0) {
            alreadyvoted.show();
        } else {
            notyetvoted.show();
        }

        function vote(rating) {
            return function inner_vote() {
                $.post(context.find("#context_url").attr('href') + '/evaluate', {
                    rating: rating
                }, function () {
                    location.reload();
                });
            };
        }

        context.find("#voting_plus").click(vote(1));
        context.find("#voting_neutral").click(vote(0));
        context.find("#voting_negative").click(vote(-1));

        delete_votings.click(function () {
            delete_votings2.toggle();
        });
        delete_votings2.click(function () {
            $.post(context.find("#context_url").attr("href") + "/clearevaluations", function () {
                location.reload();
            });
        });
    };
}(jQuery, window.collective_judgment = window.collective_judgment || {}));
