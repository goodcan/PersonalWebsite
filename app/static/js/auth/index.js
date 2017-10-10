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
    index_search($('#all-articles'), search_data, load_base_div);
});

$('#btn-refresh').click(function () {
    $('#search-content').val('')
    search_data = {
        'page': '1',
        'project_name': $('#project-search-select').val(),
        'class_name': $('#class-search-select').val(),
        'search_content': ''
    };
    index_search($('#all-articles'), search_data, load_base_div);
});

$(window).scroll(function () {
    load_page_content('/auth/index/search/', $('.load-page'), search_data, load_all_content_append);
});
