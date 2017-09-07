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

function checkPwd(p1, p2) {
    if (p1 == p2) {
        return true;
    }
};



$('#login_in').click(function () {
    $.ajax({
        url: '/auth/login/',
        type: 'POST',
        //contentType: "application/json; charset=UTF-8",
        data: JSON.stringify({
            'data':{
                'username': $('#usernameL').val(),
                'password': $('#passwordL').val(),
                'remmber_me': $("#remmber_me").is(':checked')
            }
        }),
        dataType: 'json',
    }).done(function (data, textStatus) {
        console.log(data);
    }).fail(function (xhr, err) {
        alert('请求失败，原因可能是：' + err + '！');
    });
});


$('#btn-register').click(function () {
    $p1 = $('#passwordR1');
    $p2 = $('#passwordR2');
    if (checkPwd($p1.val(), $p2.val())) {
        $p1.parent().addClass('has-success has-feedback');
        $p1.next().addClass('glyphicon glyphicon-ok form-control-feedback');
        $p1.nextUntil().show();
    }
});

$('#btn-register-cancel').click(function () {
    $p1.parentsUntil().first().removeClass().addClass('col-md-10');
    $p1.next().removeClass();
    $p1.nextUntil().hide();
});