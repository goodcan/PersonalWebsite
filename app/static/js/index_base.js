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

$('#btn-login').click(function () {
    // 生成csrf令牌
    var csrftoken = $('meta[name=csrf-token]').attr('content');
    console.log(csrftoken);

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
                'remember_me': $("#remember_me").is(':checked')
            },
        }),
        dataType: 'json',
    }).done(function (data, textStatus) {
        console.log(data);
        if (data['status'] == true) {
            if (data['data']['confirmed']) {
                $('#login-user').hide();
                $('#register-user').hide();
                $('#context-user')
                    .attr('href', '/user/' + data['data']['login_user'] + '/')
                    .html(data['data']['login_user']).show();
                $('#logout-user').show();
                $('#my-login-Modal').modal('hide');
            }
            else {
                window.location.href = 'auth/unconfirmed'
            }
        }
        else {
            errors = data['data'];
            if ('username' in errors || 'telephone' in errors) {
                $usernameL = $('#usernameL');
                if (errors['username'] != null) {
                    user_errors = errors['username']
                }
                else {
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
                'email': $('#emailR').val(),
                'password1': $('#passwordR1').val(),
                'password2': $('#passwordR2').val(),
            },
        }),
        dataType: 'json',
    }).done(function (data, textStatus) {
        console.log(data);
        if (data['status'] == true) {
            $('#my-register-Modal').modal('hide');
            // $('#my-login-Modal').modal('show');
            $('#my-message-Modal').modal('show');
            $('#message-content').html(data['data']['confirm']);
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

// 监听键盘
$('body').keydown(function () {
    // enter的键值为13
    if (event.keyCode == '13') {
        if ($('#login-form').is(':visible')) {
            $('#btn-login').click();
        }

        if ($('#register-form').is(':visible')) {
            $('#btn-register').click();
        }
    }
});

// 当弹框关闭后清楚所有输入框的内容和状态
$('#my-login-Modal, #my-register-Modal').on('hidden.bs.modal', function (e) {
    $('#my-login-Modal .form-control').val('');
    $('#my-register-Modal .form-control').val('');
    $('.clear-form-group').removeClass().addClass(FORM_STATUS[3]);
    $('.clear-glyphicon').removeClass().addClass(GLYPHICON_STATUS[3]);
    $('.clear-help').html(' ');
    // 消除注册界面跳转到登入界面后body左移
    $('body').css({'padding-right': 0});
});

// 注销后跳转到登录
$('#logout-user').click(function () {
    $.get('/auth/logout/');
    $('#login-user').show();
    $('#register-user').show();
    $('#context-user').html('').hide();
    $('#logout-user').hide();
    $('#my-login-Modal').modal('show');
    $('#usernameL').val('');
    $('#passwordL').val('');
});