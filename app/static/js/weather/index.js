clear_navbar_active();

// 初始化echarts示例mapChart
var myChart = echarts.init(document.getElementById('main'), 'dark');

//渲染的数据
// var myData = [
//
//     {name: '海门', value: [121.15, 31.89, 90]},
//     {name: '鄂尔多斯', value: [109.781327, 39.608266, 120]},
//     {name: '招远', value: [120.38, 37.35, 142]},
//     {name: '舟山', value: [122.207216, 29.985295, 123]},
// ];


var myData;

myChart.showLoading();
$.get("/weather/data.json/", function (data, status) {
    myData = data;
    // mapChart的配置
    var option = {

        title: {
            text: '全国主要城市温度',
            subtext: 'data from PM25.in',
            // sublink: 'http://www.pm25.in',
            x: 'center',
            textStyle: {
                color: '#fff'
            }
        },

        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                return params.name + ' : ' + params.value[2];
            }
        },

        //绘制地图
        geo: {
            map: 'china',

            itemStyle: {					// 定义样式
                normal: {					// 普通状态下的样式
                    areaColor: '#323c48',
                    borderColor: '#bbb'
                },
                emphasis: {					// 高亮状态下的样式
                    areaColor: '#2a333d'
                }
            }
        },
        // backgroundColor: '#404a59',  		// 图表背景色

        //绘制散点图
        series: [
            {
                name: '销量', // series名称
                type: 'scatter', // series图表类型
                coordinateSystem: 'geo', // series坐标系类型
                data: myData, // series数据内容

                itemStyle: {
                    emphasis: {
                        borderColor: '#fff',
                        borderWidth: 1
                    }
                }
            }
        ],

        //添加视觉映射组件
        visualMap: {
            type: 'continuous', // 连续型
            min: -10,       		// 值域最小值，必须参数
            max: 40,			// 值域最大值，必须参数
            calculable: true,	// 是否启用值域漫游
            inRange: {
                color: ['#50a3ba', '#eac736', '#d94e5d']
                // 指定数值从低到高时的颜色变化
            },
            textStyle: {
                color: '#fff'	// 值域控件的文本颜色
            }
        }

    };
    myChart.hideLoading();
    myChart.setOption(option);
    // console.log(myData);
});