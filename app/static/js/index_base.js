/**
 * Created by admin on 2017/9/5.
 */

$('#login-user').click(function () {
    $('#my-login-Modal').modal('show');
});


$('#register-user').click(function () {
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
            'data': {
                'username': $('#usernameL').val(),
                'password': $('#passwordL').val(),
                'remmber_me': $("#remmber_me").is(':checked')
            }
        }),
        dataType: 'json',
    }).done(function (data, textStatus) {
        console.log(data);
        if (data['status'] == true) {
            $('#login-user').hide();
            $('#register-user').hide();
            $('#context-user').html(data['data']['username']).show();
            $('#logout-user').show();
            $('#my-login-Modal').modal('hide');
        }
    }).fail(function (xhr, err) {
        alert('请求失败，原因可能是：' + err + '！');
    });
});

$('#logout-user').click(function () {
    $('#login-user').show();
    $('#register-user').show();
    $('#context-user').html('').hide();
    $('#logout-user').hide();
    $('#my-login-Modal').modal('show');
    $('#usernameL').val('');
    $('#passwordL').val('');
});

var FORM_STATUS = ['col-md-10', 'has-success has-feedback']
var GLYPHICON_STATUS = ['glyphicon glyphicon-ok form-control-feedback',
    'glyphicon glyphicon-warning-sign form-control-feedback',
    'glyphicon glyphicon-remove form-control-feedback']

function Response_status() {
    $('#btn-register').click(function () {
        $p1 = $('#passwordR1');
        $p2 = $('#passwordR2');
        if (checkPwd($p1.val(), $p2.val())) {
            $p1.parent().addClass('has-success has-feedback');
            $p1.next().addClass('glyphicon glyphicon-ok form-control-feedback');
            $p1.nextUntil().show();
        }
    });
}


$('#btn-register-cancel').click(function () {
    $p1.parentsUntil().first().removeClass().addClass('col-md-10');
    $p1.next().removeClass();
    $p1.nextUntil().hide();
});