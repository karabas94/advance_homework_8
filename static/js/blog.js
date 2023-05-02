$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-blog .modal-content").html("");
                $("#modal-blog").modal("show");
            },
            success: function (data) {
                $("#modal-blog .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {

                    $("#modal-blog").modal("hide");
                } else {
                    $("#modal-blog .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Delete book
    $("#blog-header").on("click", ".js-contact", loadForm);
    $("#modal-blog").on("submit", ".js-contact-form", saveForm);

});