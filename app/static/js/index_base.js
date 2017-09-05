/**
 * Created by admin on 2017/9/5.
 */

$('.login-button').click(function () {
    $('#my-login-Modal').modal('show');
});


$('.register-button').click(function () {
    $('#my-register-Modal').modal('show');
});

$('.my-navbar-dropdown').hover(
    function () {
        $('#my-navbar-dropdown').slideDown();
    },
    function () {
        $('#my-navbar-dropdown').slideUp();
    }
)
