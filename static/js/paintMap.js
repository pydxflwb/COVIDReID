(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['exports', 'echarts'], factory);
    } else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {
        // CommonJS
        factory(exports, require('echarts'));
    } else {
        // Browser globals
        factory({}, root.echarts);
    }
}(this, function(exports, echarts) {
    var log = function(msg) {
        if (typeof console !== 'undefined') {
            console && console.error && console.error(msg);
        }
    }
    if (!echarts) {
        log('ECharts is not Loaded');
        return;
    }
    if (!echarts.registerMap) {
        log('ECharts Map is not loaded')
        return;
    }
    echarts.registerMap('test', {
        "type": "FeatureCollection",
        "features": [{
                "type": "Feature",
                "properties": {
                    "name": "监控点1"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                121.42107009887694,
                                31.03004490080293
                            ],
                            [
                                121.42158508300781,
                                31.028941673385194
                            ],
                            [
                                121.42332315444945,
                                31.029530062931578
                            ],
                            [
                                121.42375230789185,
                                31.02879457543068
                            ],
                            [
                                121.42546892166136,
                                31.02941974016848
                            ],
                            [
                                121.42469644546507,
                                31.031221662630017
                            ],
                            [
                                121.42107009887694,
                                31.03004490080293
                            ]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "监控点2"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                121.42197132110596,
                                31.02783843318888
                            ],
                            [
                                121.42257213592531,
                                31.0264961403855
                            ],
                            [
                                121.42621994018555,
                                31.027672946057297
                            ],
                            [
                                121.42564058303833,
                                31.02901522227729
                            ],
                            [
                                121.42197132110596,
                                31.02783843318888
                            ]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "监控点3"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                121.42744302749632,
                                31.03157101099849
                            ],
                            [
                                121.42772197723387,
                                31.030780378648732
                            ],
                            [
                                121.42740011215209,
                                31.030670057333932
                            ],
                            [
                                121.42740011215209,
                                31.03041264043578
                            ],
                            [
                                121.42752885818481,
                                31.03017360983594
                            ],
                            [
                                121.4280652999878,
                                31.030339092622786
                            ],
                            [
                                121.42933130264281,
                                31.030706831119748
                            ],
                            [
                                121.42879486083984,
                                31.032030677951962
                            ],
                            [
                                121.42744302749632,
                                31.03157101099849
                            ]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "监控点4"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                121.42873048782347,
                                31.029291030116724
                            ],
                            [
                                121.42915964126587,
                                31.02826134344115
                            ],
                            [
                                121.42933130264281,
                                31.028298118156936
                            ],
                            [
                                121.42948150634766,
                                31.028279730800826
                            ],
                            [
                                121.4296531677246,
                                31.028224568711146
                            ],
                            [
                                121.43008232116699,
                                31.028316505509537
                            ],
                            [
                                121.4306616783142,
                                31.028500378840093
                            ],
                            [
                                121.43014669418336,
                                31.02980586928017
                            ],
                            [
                                121.42873048782347,
                                31.029291030116724
                            ]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "监控点5"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                121.4266276359558,
                                31.026992607051245
                            ],
                            [
                                121.42624139785767,
                                31.026698404894994
                            ],
                            [
                                121.4260697364807,
                                31.026569691165903
                            ],
                            [
                                121.42589807510376,
                                31.026349038654267
                            ],
                            [
                                121.42626285552977,
                                31.025539975071986
                            ],
                            [
                                121.42712116241454,
                                31.02590773209761
                            ],
                            [
                                121.4275074005127,
                                31.025999671132187
                            ],
                            [
                                121.42761468887329,
                                31.025999671132187
                            ],
                            [
                                121.4272928237915,
                                31.026827118450168
                            ],
                            [
                                121.42682075500488,
                                31.026624854213974
                            ],
                            [
                                121.4266276359558,
                                31.026992607051245
                            ]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "监控点6"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                121.42692804336548,
                                31.0235356743287
                            ],
                            [
                                121.4272928237915,
                                31.02178877231603
                            ],
                            [
                                121.42731428146361,
                                31.021476165419188
                            ],
                            [
                                121.42744302749632,
                                31.021255501109728
                            ],
                            [
                                121.4285159111023,
                                31.021494554088562
                            ],
                            [
                                121.42797946929932,
                                31.02377472158622
                            ],
                            [
                                121.42692804336548,
                                31.0235356743287
                            ]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "监控点7"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                121.43102645874022,
                                31.024455083574633
                            ],
                            [
                                121.43085479736327,
                                31.024307978691546
                            ],
                            [
                                121.43171310424803,
                                31.022579479300276
                            ],
                            [
                                121.43229246139526,
                                31.022358817546227
                            ],
                            [
                                121.43330097198486,
                                31.022763363704914
                            ],
                            [
                                121.43282890319823,
                                31.024087320941028
                            ],
                            [
                                121.43197059631348,
                                31.024307978691546
                            ],
                            [
                                121.43147706985474,
                                31.024455083574633
                            ],
                            [
                                121.43102645874022,
                                31.024455083574633
                            ]
                        ]
                    ]
                }
            }
        ]
    });
}));


var data = [{
        name: '监控点1',
        value: Math.round(Math.random() * 1000)
    },
    {
        name: '监控点2',
        value: Math.round(Math.random() * 1000)
    },
    {
        name: '监控点3',
        value: Math.round(Math.random() * 1000)
    },
    {
        name: '监控点4',
        value: Math.round(Math.random() * 1000)
    },
    {
        name: '监控点5',
        value: Math.round(Math.random() * 1000)
    },
    {
        name: '监控点6',
        value: Math.round(Math.random() * 1000)
    },
    {
        name: '监控点7',
        value: Math.round(Math.random() * 1000)
    }
]
var myChart = echarts.init(document.getElementById('gdMap'));
window.addEventListener('resize', function() {
    myChart.resize();
    myCharts.resize();
});
var yMax = 0;
for (var j = 0; j < data.length; j++) {
    if (yMax < data[j].value) {
        yMax = data[j].value;
    }
}
myChart.hideLoading();
var option = {
    animation: true,
    tooltip: {
        show: true
    },
    visualMap: {
        min: 0,
        max: yMax,
        text: ['高', '低'],
        orient: 'vertical',
        itemWidth: 15,
        itemHeight: 200,
        left: 0,
        bottom: 5,
        inRange: {
            color: ['#75ddff', '#0e94eb']
        },
        textStyle: {
            color: 'white'
        }
    },
    series: [{
        name: '数据名称',
        type: 'map',
        mapType: 'test',
        selectedMode: 'multiple',
        tooltip: {
            trigger: 'item',
            formatter: '{b}<br/>{c} (人)'
        },
        itemStyle: {
            normal: {
                borderWidth: 1,
                borderColor: '#0e94eb',
                label: {
                    show: false
                }
            },
            emphasis: { // 也是选中样式
                borderWidth: 1,
                borderColor: '#fff',
                backgroundColor: 'red',
                label: {
                    show: true,
                    textStyle: {
                        color: '#fff'
                    }
                }
            }
        },
        data: data,
    }]
};

myChart.setOption(option);
// myCharts.setOption(option);