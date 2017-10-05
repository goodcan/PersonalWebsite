//表单状态数组
var FORM_STATUS = [
    'form-group has-success has-feedback clear-form-group',
    'form-group has-warning has-feedback clear-form-group',
    'form-group has-error has-feedback clear-form-group',
    'form-group clear-form-group'];

//表单提示符数组
var GLYPHICON_STATUS = [
    'glyphicon glyphicon-ok form-control-feedback clear-glyphicon',
    'glyphicon glyphicon-warning-sign form-control-feedback clear-glyphicon',
    'glyphicon glyphicon-remove form-control-feedback clear-glyphicon',
    'clear-glyphicon'];

// 输入的参数没有格式问题时不显示验证后的错误信息
function clear_one_tag(tag) {
    tag.parent().removeClass().addClass(FORM_STATUS[3]);
    tag.next().removeClass().addClass(GLYPHICON_STATUS[3]);
    tag.next().next().html(' ');
}

// 显示服务器返回的验证结果
function show_tag_errors(tag, errors) {
    tag.parent().removeClass().addClass(FORM_STATUS[errors[0]]);
    tag.next().removeClass().addClass(GLYPHICON_STATUS[errors[0]]);
    tag.next().next().show().html(errors[1]);
}

// 只清除提示信息
function clear_prompting() {
    $('.clear-form-group').removeClass().addClass(FORM_STATUS[3]);
    $('.clear-glyphicon').removeClass().addClass(GLYPHICON_STATUS[3]);
    $('.clear-help').html(' ');
}

// 清楚所有表单的内容
function clear_messages() {
    $('.form-control').val('');
    clear_prompting();
}

// 清理前一个表单
function clear_prev_form() {
    $('#login-form .form-control').val('');
    $('#register-form .form-control').val('');
    clear_prompting();
}

// 弹框提示信息
function show_message(data) {
    $('#my-message-Modal').modal('show');
    $('#my-modal-title').html(data['data']['message-title']);
    $('#message-content').html(data['data']['message-content']);
}

// 清除首页active和修改注销的跳转路径
function clear_navbar_active() {
    $('#my-navbar-collapse li').removeClass('active');
}

// 加载文章和问答
function load_content($object, data) {
    var load_html = '<div class="media">' +
        '<div class="media-body">' +
        '<div class="media-heading">' +
        '<img class="media-object user-little-portrait pull-left" ' +
        'src="' + data['user_portrait_url'] + '" alt="">' +
        '<div class="title-time">' +
        '<a href="' + data['title_link'] + '" class="title-link">' + data['title'] + '</a>' +
        '<h6>' + data['create_time'] + '</h6>' +
        '</div>' +
        '</div>' +
        '<pre>' + data['body'] + '</pre>' +
        '<div class="btn-group btn-group-justified">' +
        '<a href="' + data['comment_link'] + '" class="btn btn-default btn-no-border">评论 ' +
        '<span id="comment-badge" class="badge">' + data['comment_num'] + '</span></a>' +
        '<a href="' + data['comment_link'] + '" class="btn btn-default btn-no-border">关注 ' +
        '<span id="comment-badge" class="badge">' + data['care_num'] + '</span></a>' +
        '</div>' +
        '</div>' +
        '<hr>' +
        '</div>';

    $object.prepend(load_html);
}

// 加载文章和问答的评论
function load_comment($object, data) {
    var load_html = '<div class="media">' +
        '<div class="media-left">' +
        '<a href="' + data['user_portrait_link'] + '">' +
        '<img class="media-object comment-portrait" src="' + data['user_portrait_url'] + '" alt="">' +
        '</a>' +
        '</div>' +
        '<div class="media-body">' +
        '<h4 class="media-heading">' + data['name'] + '</h4>' +
        '<h6 class="media-heading">' + data['create_time'] + '</h6>' +
        '<p>' + data['body'] + '</p>' +
        '</div>' +
        '<hr>' +
        '</div>';

    $object.prepend(load_html);
}