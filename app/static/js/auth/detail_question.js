clear_navbar_active();
update_time($('.deal-time'));
function update_care() {
    $.get('/auth/update_question_care/' + $('#question-title').attr('role') + '/',
        function (data) {
            $('#care_num').text('关注（' + data['num'] + '）');
        });
}

$('#add-question-comment').click(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/auth/add_question_comment/' + $('#question_id').val(),
        type: 'POST',
        contentType: "application/json; charset=UTF-8",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        data: JSON.stringify({
            'data': {
                'body': $('#comment_body').val()
            }
        }),
        dataType: 'json'
    }).done(function (data) {
        console.log(data);

        if (data['status'] == true) {
            clear_messages();
            show_message(data);
            load_data = data['load_data'];
            load_comment($('#question-comments'), load_data);
            $('#comment_num').text('评论（' + load_data['comment_num'] + '）');
            update_time($('#question-comments .deal-time'));
        }
        else {
            if ('url' in data['data']) {
                console.log(data['data']['url']);
                window.location.href = data['data']['url'];
            }
            show_message(data);
        }
    }).fail(function () {
        alert('请求失败！');
    });
});

$("#question-care").click(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/auth/care_question/' + $(this).attr('role') + '/' + $('#question-title').attr('role') + '/',
        type: 'GET',
        contentType: "application/json; charset=UTF-8",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
    }).done(function (data) {
        console.log(data);

        if (data['status'] == true) {
            clear_messages();
            $care_btn = $('#question-care');
            if ($care_btn.attr('role') == 'add') {
                $care_btn.removeClass('btn-success')
                    .addClass('btn-warning')
                    .text('取消关注')
                    .attr('role', 'del');
                update_care();
            }
            else {
                $care_btn.removeClass('btn-warning')
                    .addClass('btn-success')
                    .text('立即关注')
                    .attr('role', 'add');
                update_care();
            }

            show_message(data);
        }
        else {
            if ('url' in data['data']) {
                console.log(data['data']['url']);
                window.location.href = data['data']['url'];
            }
            show_message(data);
        }
    }).fail(function () {
        alert('请求失败！');
    });
});

$('body').keydown(function () {
    if (event.keyCode == '13') {
        if ($('#add-question-comment').is(':visible') && $('#btn-login').is(':hidden')) {
            $('#add-question-comment').click();
        }
    }
});

$('body').keydown(function () {
    if (event.keyCode == '13') {
        if ($('#add-article-comment').is(':visible') && $('#btn-login').is(':hidden')) {
            $('#add-article-comment').click();
        }
    }
});

$('#my-login-Modal').on('hidden.bs.modal', function (e) {
    $.get('/auth/check_question_care/' + $('#question-title').attr('role') + '/',
        function (data) {
            console.log(data['care']);
            if (data['care']) {
                $('#question-care').attr('class', 'btn btn-warning')
                    .text('取消关注')
                    .attr('role', 'del');
            }
            else {
                $('#question-care').attr('class', 'btn btn-success')
                    .text('立即关注')
                    .attr('role', 'add');
            }
        });
});