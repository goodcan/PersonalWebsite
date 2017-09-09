/**
 * Created by admin on 2017/9/5.
 */

var FORM_STATUS = [
    'form has-success has-feedback clear-form-group',
    'form has-warning has-feedback clear-form-group',
    'form has-error has-feedback clear-form-group',
    'form clear-form-group']
var GLYPHICON_STATUS = [
    'glyphicon glyphicon-ok form-control-feedback clear-glyphicon',
    'glyphicon glyphicon-warning-sign form-control-feedback clear-glyphicon',
    'glyphicon glyphicon-remove form-control-feedback clear-glyphicon',
    'clear-glyphicon']

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

// 输入的参数没有格式问题时不显示验证后的错误信息
function clear_one_tag(tag) {
    tag.parent().removeClass().addClass(FORM_STATUS[3]);
    tag.next().removeClass().addClass(GLYPHICON_STATUS[3]);
    tag.next().next().hide().html('');
}

// 显示服务器返回的验证结果
function show_tag_errors(tag, errors) {
    tag.parent().removeClass().addClass(FORM_STATUS[errors[0]]);
    tag.next().removeClass().addClass(GLYPHICON_STATUS[errors[0]]);
    tag.next().next().show().html(errors[1]);
}

$('#btn-login').click(function () {
    // 生成csrf令牌
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    // 发起ajax请求
    $.ajax({
        url: '/auth/login/',
        type: 'POST',
        contentType: "application/json; charset=UTF-8",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        data: JSON.stringify({
            'data': {
                'username': $('#usernameL').val(),
                'password': $('#passwordL').val(),
                'remmber_me': $("#remmber_me").is(':checked')
            },
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
        else {
            errors = data['data'];
            if ('username' in errors) {
                $usernameL = $('#usernameL');
                user_errors = errors['username']
                show_tag_errors($usernameL, user_errors)
            }
            else {
                $usernameL = $('#usernameL');
                clear_one_tag($usernameL);
            }

            if ('password' in errors) {
                $passwordL = $('#passwordL');
                pwd_errors = errors['password']
                show_tag_errors($passwordL, pwd_errors)
            }
            else {
                $passwordL = $('#passwordL');
                clear_one_tag($passwordL);
            }
        }
    }).fail(function (xhr, err) {
        alert('请求失败！');
    });
});

$('#btn-register').click(function () {
    // 生成csrf令牌
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    // 发起ajax请求
    $.ajax({
        url: '/auth/register/',
        type: 'POST',
        contentType: "application/json; charset=UTF-8",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        data: JSON.stringify({
            'data': {
                'username': $('#usernameR').val(),
                'telephone': $('#telephoneR').val(),
                'password1': $('#passwordR1').val(),
                'password2': $('#passwordR2').val(),
            },
        }),
        dataType: 'json',
    }).done(function (data, textStatus) {
        console.log(data);
        if (data['status'] == true) {
           $('#my-register-Modal').modal('hide');
           $('#my-login-Modal').modal('show');
        }
        else {
            errors = data['data'];
            if ('username' in errors) {
                $usernameR = $('#usernameR');
                user_errors = errors['username']
                show_tag_errors($usernameR, user_errors)
            }
            else {
                $usernameR = $('#usernameR');
                clear_one_tag($usernameR);
            }

            if ('telephone' in errors) {
                $telephoneR = $('#telephoneR');
                pwd_errors = errors['telephone']
                show_tag_errors($telephoneR, pwd_errors)
            }
            else {
                $telephoneR = $('#telephoneR');
                clear_one_tag($telephoneR);
            }

            if ('password1' in errors) {
                $passwordR1 = $('#passwordR1');
                pwd_errors = errors['password1']
                show_tag_errors($passwordR1, pwd_errors)
            }
            else {
                $passwordR1 = $('#passwordR1');
                clear_one_tag($passwordR1);
            }

            if ('password2' in errors) {
                $passwordR2 = $('#passwordR2');
                pwd_errors = errors['password2']
                show_tag_errors($passwordR2, pwd_errors)
            }
            else {
                $passwordR2 = $('#passwordR2');
                clear_one_tag($passwordR2);
            }
        }
    }).fail(function (xhr, err) {
        alert('请求失败！');
    });
});

$('#my-login-Modal, #my-register-Modal').on('hidden.bs.modal', function (e) {
    $('#my-login-Modal .form-control').val('');
    $('.clear-form-group').removeClass().addClass(FORM_STATUS[3]);
    $('.clear-glyphicon').removeClass().addClass(GLYPHICON_STATUS[3]);
    $('.clear-help').hide().html('');
    // 消除注册界面跳转到登入界面后body左移
    $('body').css({'padding-right': 0});
})

$('#logout-user').click(function () {
    $('#login-user').show();
    $('#register-user').show();
    $('#context-user').html('').hide();
    $('#logout-user').hide();
    $('#my-login-Modal').modal('show');
    $('#usernameL').val('');
    $('#passwordL').val('');
});