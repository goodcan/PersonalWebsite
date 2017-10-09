clear_navbar_active();

$('#btn-search').click(function () {
    data = {
        'project_name': $('#project-search-select').val(),
        'class_name': $('#class-search-select').val(),
        'search_content': $('#search-content').val()
    }
    $.get('/auth/index/search/', data, function (data) {
         $('#all-articles').html('');
            load_data = data['data']['load_data'];
            l = load_data.length;
            for (i = 0; i < l; i++) {
                load_all_content_append($('#all-articles'), load_data[i]);
            }
    });
});