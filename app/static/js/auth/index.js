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
    load_page_content(search_data);
});
