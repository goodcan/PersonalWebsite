// 清除首页active和修改注销的跳转路径
$('#my-navbar-collapse li').removeClass('active');
$('#logout-user').click(function () {
    window.location.href = "/auth/login/";
});

// 自动调节图片大小
function show_user_picture() {
    $character_portrait = $('#user-portrait');
    $character_portrait.css({'height': $character_portrait.width()});
}

show_user_picture();
$(window).resize(function () {
    show_user_picture();
});

// 选项卡特效
$('.panel-body').hide().first().show();
$('.panel-heading').click(function () {
    $(this).next().slideDown();
    $('.panel-body').not($(this).next()).slideUp();
});