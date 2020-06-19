$(document).ready(function () {
    $('button:submit').on('click', function() {
        $(this).prop('disabled', true);
        $(this).parent().parent('form').submit();
        setTimeout(() => {
            $(this).prop('disabled', false);
        }, 2000);
    });
});