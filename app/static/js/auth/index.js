clear_navbar_active();

$('#btn-search').click(function () {
    data = {
        'class_name': $('#search-select').val(),
        'search_content': $('#search-content').val()
    }
    $.get('/auth/index/search/', data, function (data) {
         $('#all-articles').html('');
            load_data = data['data']['load_data'];
            l = load_data.length;
            for (i = 0; i < l; i++) {
                index_load_content($('#all-articles'), load_data[i]);
            }
    });
});