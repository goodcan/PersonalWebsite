$atFirst = $('.paging a').first();
$atLast = $('.paging a').last();
$('.paging').prepend($atLast.prop('outerHTML')).append($atFirst.prop('outerHTML')).show();
$('.paging a').first().next().addClass('active');
$('.paging a').first().attr('rel', '-1').hide();
$('.paging a').last().attr('rel', '0').hide();

var imageWidth = $('.mycarousel').width();
var imageHeight = $('.mycarousel').height();
$atFirst = $('.images-reel a').first();
$atLast = $('.images-reel a').last();
$('.images-reel').prepend($atLast.prop('outerHTML')).append($atFirst.prop('outerHTML'));

//计算一共有几张图片，即计算在.images-reel中几个img
var imageSum = $('.images-reel img').length;
//计算总宽度
var imageReelWidth = imageWidth * imageSum;
$('.images-reel').css({'width': imageReelWidth, 'left': -imageWidth});
$('.images-reel img').css({'width': imageWidth, 'height': imageHeight});


function rotate() {
    var triggerID = $active.attr('rel') - 1;

    if (triggerID == -1) {
        $('.images-reel').animate({
            left: -imageReelWidth + imageWidth
        }, 500, function () {
            $('.images-reel').css({'left': -imageWidth});
        });

        $('.paging a').removeClass('active');
        $('.paging a').first().next().addClass('active');
    }
    else {
        if (triggerID == -2) {
            $('.images-reel').animate({
                left: 0
            }, 500, function () {
                $('.images-reel').css({'left': -imageWidth * (imageSum - 2)});
            });

            $('.paging a').removeClass('active');
            $('.paging a').last().prev().addClass('active');
        }
        else {
            var image_reelPosition = (triggerID + 1) * imageWidth;
            //启动动画
            $('.images-reel').animate({
                left: -image_reelPosition
            }, 500);

            $('.paging a').removeClass('active');
            $active.addClass('active');
        }
    }
}

function rotateSwitch() {
    play = setInterval(function () {
        $active = $('.paging a.active').next();
        rotate();
    }, 5000);
}

rotateSwitch();

$('.paging a').click(function () {
    $('.paging a').not($(this)).removeClass('active');
    $(this).addClass('active');
    $active = $(this);
    //立即停止动画
    clearInterval(play);
    //设定开始位置
    rotate();
    //重启动画
    rotateSwitch();
    //取消跳转
    return false;
});

//鼠标进入后停止动画，滑出后继续动画
$('.images-reel a').hover(
    function () {
        clearInterval(play);
    },
    function () {
        rotateSwitch();
    }
);

$('.left-control').click(function () {
    $active = $('.paging a.active').prev();
    clearInterval(play);
    rotate();
    rotateSwitch();
});

$('.right-control').click(function () {
    $active = $('.paging a.active').next();
    clearInterval(play);
    rotate();
    rotateSwitch();
});

$(window).resize(function () {
    clearInterval(play);
    imageWidth = $('.mycarousel').width();
    imageHeight = $('.mycarousel').height();
    imageReelWidth = imageWidth * imageSum;
    $nowActive = $('.paging a.active');
    $('.images-reel').css({'width': imageReelWidth, 'left': -imageWidth * $nowActive.attr('rel')});
    $('.images-reel img').css({'width': imageWidth, 'height': imageHeight});
    rotateSwitch();
});