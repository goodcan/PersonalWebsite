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

// 主登录界面 清理前一个表单
function clear_prev_form_only() {
    $('#login-form-only .form-control').val('');
    $('#register-form-only .form-control').val('');
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
