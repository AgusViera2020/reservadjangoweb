$(document).ready(function() {
    $('#id_email').on('input', function() {
        var email = $(this).val();
        $.ajax({
            url: '/accounts/email_check/',
            data: {
                'email': email
            },
            dataType: 'json',
            success: function(data) {
                if (data.available) {
                    $('#id_email').css('border-color', 'green');
                    $('#email-note').text('El correo está disponible').css('color', 'green');
                } else {
                    $('#id_email').css('border-color', 'red');
                    $('#email-note').text('Ya existe una cuenta con este email.').css('color', 'red');
                }
            }
        });
    });
});