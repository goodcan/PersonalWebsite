// 清除首页active和修改注销的跳转路径
$('#my-navbar-collapse li').removeClass('active');
$('#logout-user-profile').click(function () {
    window.location.href = "/auth/login/";
});

// 自动调节图片大小
function show_user_picture() {
    $character_portrait = $('#user-portrait');
    $character_portrait.css({'height': $character_portrait.width()});
}

show_user_picture();
$(window).resize(function () {
    show_user_picture();
});

// 选项卡特效
$('.panel-body').hide().first().show();
$('.panel-heading').click(function () {
    $(this).next().slideDown();
    $('.panel-body').not($(this).next()).slideUp();
});

$('#setting-btn-list .list-group-item').click(function () {
    clear_messages();
    $click_tag = $(this);
    $('#setting-btn-list .list-group-item').removeClass('active');
    $click_tag.addClass('active');
    $('.setting-content').hide();
    $('#' + $click_tag.attr('id') + '-content').show();
});

$('#btn-resetpwd').click(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/auth/reset_password_request/',
        type: 'POST',
        contentType: "application/json; charset=UTF-8",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        data: JSON.stringify({
            'data': {
                'email': $('#emailRS').val(),
                'passwordRS1': $('#passwordRS1').val(),
                'passwordRS2': $('#passwordRS2').val()
            }
        }),
        dataType: 'json'
    }).done(function (data) {
        console.log(data);

        if (data['status'] == true) {
            clear_messages();
            show_message(data);
        }
        else {
            errors = data['data'];
            if ('email' in errors) {
                $email = $('#emailRS');
                email_errors = errors['email']
                show_tag_errors($email, email_errors)
            }
            else {
                $email = $('#email');
                clear_one_tag($email);
            }

            if ('password1' in errors) {
                $passwordRS1 = $('#passwordRS1');
                pwd1_errors = errors['password1']
                show_tag_errors($passwordRS1, pwd1_errors)
            }
            else {
                $passwordRS1 = $('#passwordRS1');
                clear_one_tag($passwordRS1);
            }

            if ('password2' in errors) {
                $passwordRS2 = $('#passwordRS2');
                pwd2_errors = errors['password2']
                show_tag_errors($passwordRS2, pwd2_errors)
            }
            else {
                $passwordRS2 = $('#passwordRS2');
                clear_one_tag($passwordRS2);
            }
        }
    }).fail(function () {
        alert('请求失败！');
    });
});

$('#btn-resetemail').click(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/auth/reset_email_request/',
        type: 'POST',
        contentType: "application/json; charset=UTF-8",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        data: JSON.stringify({
            'data': {
                'oldEmailRS': $('#old-emailRS').val(),
                'newEmailRS': $('#new-emailRS').val()
            }
        }),
        dataType: 'json'
    }).done(function (data) {
        console.log(data);

        if (data['status'] == true) {
            clear_messages();
            show_message(data);
        }
        else {
            errors = data['data'];
            if ('oldEmail' in errors) {
                oldEmail = $('#old-emailRS');
                err = errors['oldEmail']
                show_tag_errors(oldEmail, err)
            }
            else {
                oldEmail = $('#old-emailRS');
                clear_one_tag(oldEmail);
            }

            if ('newEmail' in errors) {
                $newEmail = $('#new-emailRS');
                err = errors['newEmail']
                show_tag_errors($newEmail, err)
            }
            else {
                $newEmail = $('#new-emailRS');
                clear_one_tag($newEmail);
            }
        }
    }).fail(function () {
        alert('请求失败！');
    });
});

$('#btn-set-information').click(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/auth/set_information/',
        type: 'POST',
        contentType: "application/json; charset=UTF-8",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        data: JSON.stringify({
            'data': {
                'name': $('#set-name').val(),
                'location': $('#set-location').val(),
                'about_me': $('#set-about-me').val()
            }
        }),
        dataType: 'json'
    }).done(function (data) {
        console.log(data);

        if (data['status'] == true) {
            $('#user-content h2 strong').html($('#set-name').val());
            $('#user-content h5').html($('#set-location').val());
            if ($('#set-about-me').val() == '') {
                $('#user-content p').html('');
            }
            else {
                 $('#user-content p').html('“' + $('#set-about-me').val() + '”');
            }
            show_message(data);
        }
        else {
            show_message(data);
        }
    }).fail(function () {
        alert('请求失败！');
    });
});

// 监听键盘
$('body').keydown(function () {
    // enter的键值为13
    if (event.keyCode == '13') {
        if ($('#setting-0-content').is(':visible')) {
            $('#btn-set-information').click();
        }
        if ($('#setting-1-content').is(':visible')) {
            $('#btn-resetpwd').click();
        }
        if ($('#setting-2-content').is(':visible')) {
            $('#btn-resetemail').click();
        }
    }
});

$('.btn-cancel').click(function () {
    clear_messages();
});