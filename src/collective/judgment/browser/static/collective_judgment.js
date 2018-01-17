/*global location: false, window: false, jQuery: false */
(function ($, collective_judgment) {
    "use strict";
    collective_judgment.init_voting_viewlet = function (context) {
        var notyetevaluated = context.find("#notyetevaluated"),
            alreadyevaluated = context.find("#alreadyevaluated"),
            delete_votings = context.find("#delete_evaluations"),
            delete_votings2 = context.find("#delete_evaluations2");

        if (context.find("#evaluated").length !== 0) {
            alreadyevaluated.show();
        } else {
            notyetevaluated.show();
        }

        function evaluate(rating) {
            return function inner_evaluate() {
                $.post(context.find("#context_url").attr('href') + '/evaluate', {
                    rating: rating
                }, function () {
                    location.reload();
                });
            };
        }

        context.find("#evaluation_approve").click(evaluate("approve"));
        context.find("#evaluation_disapprove").click(evaluate("disapprove"));

        delete_evaluations.click(function () {
            delete_evaluations2.toggle();
        });
        // delete_evaluations2.click(function () {
        //     $.post(context.find("#context_url").attr("href") + "/clearevaluations", function () {
        //         location.reload();
        //     });
        // });
    };
}(jQuery, window.collective_judgment = window.collective_judgment || {}));
