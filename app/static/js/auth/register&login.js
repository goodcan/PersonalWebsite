/**
 * Created by admin on 2017/9/9.
 */

function show_login_form() {
    $('#login-form-only').show();
    $('#register-form-only').hide();
}

function show_register_form() {
    $('#login-form-only').hide();
    $('#register-form-only').show();
}

if ($('.title-active').text() == '登录') {
    show_login_form();
}
else if ($('.title-active').text() == '注册') {
    show_register_form();
}

clear_navbar_active();

$('.login-title').click(function () {
    $(this).addClass('title-active');
    $(this).siblings().removeClass('title-active');
    show_login_form();
    clear_prev_form_only();
});

$('.register-title').click(function () {
    $(this).addClass('title-active');
    $(this).siblings().removeClass('title-active');
    show_register_form();
    clear_prev_form_only();
});

$('#btn-login-only').click(function () {
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
                'username': $('#usernameLO').val(),
                'password': $('#passwordLO').val(),
                'remember_me': $("#remember_me").is(':checked')
            },
        }),
        dataType: 'json'
    }).done(function (data, textStatus) {
            // console.log(data);

            if (data['status'] == true) {
                location.href = data['data']['redirect'];
            }
            else {
                errors = data['data'];
                if ('username' in errors || 'telephone' in errors) {
                    $usernameL = $('#usernameLO');
                    if (errors['username'] != null) {
                        user_errors = errors['username']
                    }
                    else {
                        user_errors = errors['telephone']
                    }
                    show_tag_errors($usernameL, user_errors)
                }
                else {
                    $usernameL = $('#usernameLO');
                    clear_one_tag($usernameL);
                }

                if ('password' in errors) {
                    $passwordL = $('#passwordLO');
                    pwd_errors = errors['password']
                    show_tag_errors($passwordL, pwd_errors)
                }
                else {
                    $passwordL = $('#passwordLO');
                    clear_one_tag($passwordL);
                }
            }
        }
    ).fail(function (xhr, data) {
        alert('请求失败！');
    });
});

$('#btn-register-only').click(function () {
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
                'username': $('#usernameRO').val(),
                'telephone': $('#telephoneRO').val(),
                'email': $('#emailRO').val(),
                'password1': $('#passwordR1O').val(),
                'password2': $('#passwordR2O').val(),
            },
        }),
        dataType: 'json',
    }).done(function (data, textStatus) {
        // console.log(data);
        if (data['status'] == true) {
            $('.login-title').addClass('title-active');
            $('.login-title').siblings().removeClass('title-active');
            show_login_form();
            clear_prev_form_only();
            // alert(data['data']['confirm'])
            show_message(data);
        }
        else {
            errors = data['data'];
            if ('username' in errors) {
                $usernameR = $('#usernameRO');
                err = errors['username']
                show_tag_errors($usernameR, err)
            }
            else {
                $usernameR = $('#usernameRO');
                clear_one_tag($usernameR);
            }

            if ('telephone' in errors) {
                $telephoneR = $('#telephoneRO');
                err = errors['telephone']
                show_tag_errors($telephoneR, err)
            }
            else {
                $telephoneR = $('#telephoneRO');
                clear_one_tag($telephoneR);
            }

            if ('email' in errors) {
                $emailR = $('#emailRO');
                err = errors['email']
                show_tag_errors($emailR, err)
            }
            else {
                $emailR = $('#emailRO');
                clear_one_tag($emailR);
            }

            if ('password1' in errors) {
                $passwordR1 = $('#passwordR1O');
                err = errors['password1']
                show_tag_errors($passwordR1, err)
            }
            else {
                $passwordR1 = $('#passwordR1O');
                clear_one_tag($passwordR1);
            }

            if ('password2' in errors) {
                $passwordR2 = $('#passwordR2O');
                err = errors['password2']
                show_tag_errors($passwordR2, err)
            }
            else {
                $passwordR2 = $('#passwordR2O');
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
        if ($('#login-form-only').is(':visible')) {
            $('#btn-login-only').click();
        }

        if ($('#register-form-only').is(':visible')) {
            $('#btn-register-only').click();
        }
    }
});