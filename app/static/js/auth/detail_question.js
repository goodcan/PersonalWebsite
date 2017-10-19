clear_navbar_active();

var LOAD_DATA = {
    'page': '1',
    'question_id': $('#question-comments').attr('role')
};

var load_Q_comment_div = '<div class="load-Q-comment" name="2"></div>';

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
        // console.log(data);

        if (data['status'] == true) {
            clear_messages();
            show_message(data);
            load_data = data['load_data'];
            $('#question-comments').html('');
            for (i = 0; i < load_data.length; i++) {
                load_comment_append($('#question-comments'), load_data[i]);
            }
            $("#question-comments").append(load_Q_comment_div);
            $('#comment_num').text('评论（' + data['comment_num'] + '）');
        }
        else {
            if ('url' in data['data']) {
                // console.log(data['data']['url']);
                // window.location.href = data['data']['url'];
                $('#my-login-Modal').modal('show');
            }
            else {
                show_message(data);
            }
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
        // console.log(data);

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
                // console.log(data['data']['url']);
                // window.location.href = data['data']['url'];
                $('#my-login-Modal').modal('show');
            }
            else {
                show_message(data);
            }
        }
    }).fail(function () {
        alert('请求失败！');
    });
});

$('body').keydown(function () {
    if (event.keyCode == '13') {
        if ($('#add-question-comment').is(':visible')
            && $('#btn-login').is(':hidden')
            && $('#btn-register').is(':hidden')) {
            $('#add-question-comment').click();
        }
    }
});

$('#my-login-Modal').on('hidden.bs.modal', function (e) {
    $.get('/auth/check_question_care/' + $('#question-title').attr('role') + '/',
        function (data) {
            // console.log(data['care']);
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

$(window).scroll(function () {
    load_page_content('/auth/load_question_comment_page/', $('.load-Q-comment'), LOAD_DATA, load_comment_append);
});