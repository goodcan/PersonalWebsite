clear_navbar_active();

$('#add-article-comment').click(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/auth/add_article_comment/' + $('#article_id').val(),
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
            load_comment($("#article-comments"), load_data);
            $('#article-comment b').text('评论（' + load_data['comment_num'] + '）：');
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

$("#article-care").click(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/auth/care_article/' + $(this).attr('role') + '/' + $('#article-title').attr('role') + '/',
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
            $care_btn = $('#article-care');
            if ($care_btn.attr('role') == 'add') {
                $care_btn.removeClass('btn-success')
                    .addClass('btn-warning')
                    .text('取消关注')
                    .attr('role', 'del');
            }
            else {
                $care_btn.removeClass('btn-warning')
                    .addClass('btn-success')
                    .text('立即关注')
                    .attr('role', 'add');
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
        if ($('#add-article-comment').is(':visible') && $('#btn-login').is(':hidden')) {
            $('#add-article-comment').click();
        }
    }
});

$('#my-login-Modal').on('hidden.bs.modal', function (e) {
    $.get('/auth/check_article_care/' + $('#article-title').attr('role') + '/',
        function (data) {
            console.log(data['care']);
            if (data['care']) {
                $('#article-care').attr('class', 'btn btn-warning')
                    .text('取消关注')
                    .attr('role', 'del');
            }
            else {
                $('#article-care').attr('class', 'btn btn-success')
                    .text('立即关注')
                    .attr('role', 'add');
            }
        });
});