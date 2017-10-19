clear_navbar_active();

var LOAD_DATA = {
    'page': '1',
    'article_id': $('#article-comments').attr('role')
};

var load_A_comment_div = '<div class="load-A-comment" name="2"></div>';

function update_care() {
    $.get('/auth/update_article_care/' + $('#article-title').attr('role') + '/',
        function (data) {
            $('#care_num').text('关注（' + data['num'] + '）');
        });
}

$('#add-article-comment').click(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajax({
        url: '/auth/add_article_comment/',
        type: 'POST',
        contentType: "application/json; charset=UTF-8",
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        },
        data: JSON.stringify({
            'data': {
                'article_id': $('#article_id').val(),
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
            $("#article-comments").html('');
            for (i = 0; i < load_data.length; i++) {
                load_comment_append($("#article-comments"), load_data[i]);
            }
            $("#article-comments").append(load_A_comment_div);
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
        // console.log(data);

        if (data['status'] == true) {
            clear_messages();
            $care_btn = $('#article-care');
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
        if ($('#add-article-comment').is(':visible')
            && $('#btn-login').is(':hidden')
            && $('#btn-register').is(':hidden')) {
            $('#add-article-comment').click();
        }
    }
});

$('#my-login-Modal').on('hidden.bs.modal', function (e) {
    $.get('/auth/check_article_care/' + $('#article-title').attr('role') + '/',
        function (data) {
            // console.log(data['care']);
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

$(window).scroll(function () {
    load_page_content('/auth/load_article_comment_page/', $('.load-A-comment'), LOAD_DATA, load_comment_append);
});