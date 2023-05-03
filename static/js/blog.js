(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
})()

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
                    $('#modal-blog .modal-content').html('<div class="text-center">Message sent!</div>');
                    setTimeout(function () {
                        $('#modal-blog').modal('hide');
                    }, 3000);
                } else {
                    $("#modal-blog .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Сontact form
    $("#blog-header").on("click", ".js-contact", loadForm);
    $("#modal-blog").on("submit", ".js-contact-form", saveForm);

});