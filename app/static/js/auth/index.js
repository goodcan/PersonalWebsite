clear_navbar_active();

var search_data = {
        'page': '1',
        'project_name': $('#project-search-select').val(),
        'class_name': $('#class-search-select').val(),
        'search_content': $('#search-content').val()
    };

var load_base_div = $('.load-page').prop('outerHTML');

$('#btn-search').click(function () {
    search_data = {
        'page': '1',
        'project_name': $('#project-search-select').val(),
        'class_name': $('#class-search-select').val(),
        'search_content': $('#search-content').val()
    };
    $.get('/auth/index/search/', search_data, function (data) {
        $('#all-articles').html('');
        load_data = data['data']['load_data'];
        l = load_data.length;
        for (i = 0; i < l; i++) {
            load_all_content_append($('#all-articles'), load_data[i]);
        }
        $('#all-articles').append(load_base_div);
    });
});

$(window).scroll(function () {
    var wh = $(window).height();
    var sh = $(window).scrollTop();
    // var dh = $('#all-articles hr:last').offset().top;
    $('.load-page').each(function () {
        $target = $(this);
        dh = $target.offset().top;
        console.log(sh);
        console.log(dh);
        console.log(wh);
        console.log(dh - sh);
        if ((dh - sh) <= wh) {
            $target.removeClass('load-page');
            $target.after($target.prop('outerHTML'));
            search_data['page'] = $target.attr('name'),
            console.log($target.attr('name'));
            $.get('/auth/index/search/', search_data, function (data) {
                if (data['status']) {
                    load_data = data['data']['load_data'];
                    l = load_data.length;
                    for (i = 0; i < l; i++) {
                        load_all_content_append($target, load_data[i]);
                    }
                    $target.next()
                        .attr('name', data['data']['next_page'])
                        .addClass('load-page');

                    if (data['data']['next_page'] == null) {
                        $target.next().removeClass('load-page')
                            .css({'text-align': 'center'})
                            .html('<h4>已加载全部内容</h4>');
                    }
                }
                else {
                    $target.css({'text-align': 'center'})
                        .html('<h4>' + data['data']['message'] + '</h4>');
                }
            });
        }
    });
});