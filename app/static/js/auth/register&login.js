/**
 * Created by admin on 2017/9/9.
 */

//表单状态数组
var FORM_STATUS = [
    'form has-success has-feedback clear-form-group',
    'form has-warning has-feedback clear-form-group',
    'form has-error has-feedback clear-form-group',
    'form clear-form-group']

//表单提示符数组
var GLYPHICON_STATUS = [
    'glyphicon glyphicon-ok form-control-feedback clear-glyphicon',
    'glyphicon glyphicon-warning-sign form-control-feedback clear-glyphicon',
    'glyphicon glyphicon-remove form-control-feedback clear-glyphicon',
    'clear-glyphicon']

// 输入的参数没有格式问题时不显示验证后的错误信息
function clear_one_tag(tag) {
    tag.parent().removeClass().addClass(FORM_STATUS[3]);
    tag.next().removeClass().addClass(GLYPHICON_STATUS[3]);
    tag.next().next().html(' ');
}

// 显示服务器返回的验证结果
function show_tag_errors(tag, errors) {
    tag.parent().removeClass().addClass(FORM_STATUS[errors[0]]);
    tag.next().removeClass().addClass(GLYPHICON_STATUS[errors[0]]);
    tag.next().next().show().html(errors[1]);
}

// 清理前一个表单
function clear_prev_form() {
    $('#login-form .form-control').val('');
    $('#register-form .form-control').val('');
    $('.clear-form-group').removeClass().addClass(FORM_STATUS[3]);
    $('.clear-glyphicon').removeClass().addClass(GLYPHICON_STATUS[3]);
    $('.clear-help').html(' ');
}

if ($('.title-active').text() == '登录') {
    $('#login-form').show();
    $('#register-form').hide();
}
else if ($('.title-active').text() == '注册') {
    $('#login-form').hide();
    $('#register-form').show();
}

$('.login-title').click(function () {
    $(this).addClass('title-active');
    $(this).siblings().removeClass('title-active');
    $('#login-form').show();
    $('#register-form').hide();
    clear_prev_form();
});

$('.register-title').click(function () {
    $(this).addClass('title-active');
    $(this).siblings().removeClass('title-active');
    $('#login-form').hide();
    $('#register-form').show();
    clear_prev_form();
});

$('#btn-login').click(function () {
    // 生成csrf令牌
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    // 发起ajax请求
    $.ajax({
        url: window.location.href,
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
                'remember_me': $("#remember_me").is(':checked')
            },
        }),
        dataType: 'json'
    }).done(function (data, textStatus) {
            console.log(data);

            if (data['status'] == true) {
                location.href = data['data']['redirect'];
            }
            else {
                errors = data['data'];
                if ('username' in errors || 'telephone' in errors) {
                    $usernameL = $('#usernameL');
                    if (errors['username'] != null) {
                        user_errors = errors['username']
                    }
                    else
                    {
                        user_errors = errors['telephone']
                    }
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
        }
    ).fail(function (xhr, data) {
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
                'email': $('#emailR').val(),
                'password1': $('#passwordR1').val(),
                'password2': $('#passwordR2').val(),
            },
        }),
        dataType: 'json',
    }).done(function (data, textStatus) {
        console.log(data);
        if (data['status'] == true) {
            $('.login-title').addClass('title-active');
            $('.login-title').siblings().removeClass('title-active');
            $('#login-form').show();
            $('#register-form').hide();
            clear_prev_form();
            // alert(data['data']['confirm'])
            $('#my-message-Modal').modal('show');
            $('#message-content').html(data['data']['confirm']);
        }
        else {
            errors = data['data'];
            if ('username' in errors) {
                $usernameR = $('#usernameR');
                err = errors['username']
                show_tag_errors($usernameR, err)
            }
            else {
                $usernameR = $('#usernameR');
                clear_one_tag($usernameR);
            }

            if ('telephone' in errors) {
                $telephoneR = $('#telephoneR');
                err = errors['telephone']
                show_tag_errors($telephoneR, err)
            }
            else {
                $telephoneR = $('#telephoneR');
                clear_one_tag($telephoneR);
            }

            if ('email' in errors) {
                $emailR = $('#emailR');
                err = errors['email']
                show_tag_errors($emailR, err)
            }
            else {
                $emailR = $('#emailR');
                clear_one_tag($emailR);
            }

            if ('password1' in errors) {
                $passwordR1 = $('#passwordR1');
                err = errors['password1']
                show_tag_errors($passwordR1, err)
            }
            else {
                $passwordR1 = $('#passwordR1');
                clear_one_tag($passwordR1);
            }

            if ('password2' in errors) {
                $passwordR2 = $('#passwordR2');
                err = errors['password2']
                show_tag_errors($passwordR2, err)
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

// 监听键盘
$('body').keydown(function () {
    // enter的键值为13
    if (event.keyCode == '13') {
        if ($('#login-form').is(':hidden')) {
            $('#btn-register').click();
        }

        if ($('#register-form').is(':hidden')) {
            $('#btn-login').click();
        }
    }
});