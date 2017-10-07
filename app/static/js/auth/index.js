clear_navbar_active();

$('#btn-search').click(function () {
    $.get('/auth/index/search/' + $('#search-content').val() + '/', function (data) {
         $('#all-articles').html('');
            load_data = data['data']['load_data'];
            l = load_data.length;
            for (i = 0; i < l; i++) {
                load_content($('#all-articles'), load_data[i]);
            }
    });
});