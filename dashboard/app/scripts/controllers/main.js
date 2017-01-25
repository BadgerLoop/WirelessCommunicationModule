'use strict';
/**
 * @ngdoc function
 * @name sbAdminApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sbAdminApp
 */
angular.module('sbAdminApp')
   .controller('MainCtrl', function($scope,$position,NgTableParams,$riffle,$http) {

    //INITIALIZE SCOPE VARIABLES
    $scope.d3_api
    $scope.hb_interval = 250
    $scope.hb_on = false
    $scope.hb_fault_tollerance = 0
    $scope.msgTypes = []
    $scope.parser = {}
    $scope.system_status = "GOOD"
    $scope.colors = {
        green: "#00FF00",
        yellow : "#FFFF00",
        red: "#FF0000"
    }
    $scope.states = [
                {name:'FAULT', value:'00',level: 'danger'},
                {name:'IDLE',value:'01',level: 'success'},
                {name:'READY',value: '02',level: 'success'},
                {name:'PUSHING',value: '03',level: 'success'},
                {name:'COAST',value: '04',level: 'success'},
                {name:'BRAKING',value: '05',level: 'warning'}, 
                {name:'EMERGENCY_BRAKING' ,value: '06',level: 'danger'},
                {name:'FRONT_AXLE_BRAKING' ,value: '07',level: 'danger'},
                {name:'REAR_AXLE_BRAKING' ,value: '08',level: 'danger'},
                {name:'WAITING_FOR_SAFE' ,value: '09',level: 'warning'},
                {name:'SAFE' ,value: '0A',level: 'success'}
                ]


    var set_up_scope = function(parser){
        for ( var i = 0; i< parser.messages.length; i++){
            //Set up command messages
            var message = parser.messages[i]
            if (parser.messages[i].cmd) {
                    var comand = parser.messages[i]
                    $scope.msgTypes.push(comand)
            }
            else {
                for (var g = 0; g < message.values.length; g++){
                    //console.log(parser.msg_type[key].values[i])
                    //console.log(value_name)
                    var value = message.values[g]
                    $scope[value.title] = {
                                            max: value.nominal_high,
                                            min: value.nominal_low,
                                            val: null,
                                            status_style: 'info'
                                            }
                }
            }
        }
        //console.log($scope)
        console.log("Updated Scope variables")
    }
    //INITIALIZE PARSER FROM CONFIG FILE
    $http.get('../../parser.json').success(function(data) {
            $scope.parser = data
            console.log($scope.parser)
            console.log("Parser read successfully")
            set_up_scope($scope.parser)
    });


    //INITIALIZE MODULE SCOPE VARIABLES
    $scope.WCM = {}
    $scope.MCM = {}
    $scope.VNM = {}
    $scope.VSM = {}
    $scope.BCM = {}
    $scope.BMS = {}

    $scope.update_states  = function(sid,data){
        var modules = Object.keys($scope.parser.SID)
        console.log(modules)
        console.log(data)
        for(var u = 0; u<modules.length; u++){
            var sid_from_mask = $scope.parser.SID[modules[u]].from
            console.log(sid_from_mask)
            if (((sid_from_mask & parseInt(sid,16)) === sid_from_mask) && (modules[u] !== "NONE")) {
                //Hopefully this works
                console.log('update status of: ' + modules[u]) 
                $scope[modules[u]+'_state'].curr=$scope.states[data[1]]

                // $scope[modules[u]+'_state'].prev=$scope.states[parseInt(data[3],16)].name
                // $scope[modules[u]+'_state'].next=$scope.states[parseInt(data[4],16)].name
                console.log("updated: "+ modules[u] +" State to: " +$scope[modules[u]+'_state'].curr.name)
            }
        } 
    }
    $scope.toggle_heartbeat = function(op){
        console.log("updating heartbeat")
        $riffle.publish("hb_ctrl",[op,$scope.hb_interval,$scope.hb_fault_tollerance])
        console.log("Sent: " + [op,$scope.hb_interval,$scope.hb_fault_tollerance] + " to hb_ctrl")
        if (op ==1){
            $scope.hb_on = true
        } else {
            $scope.hb_on = false
        }
    }

///////////////Admin/////////////////////////////////
    $scope.templates = [{
      label: 'Heartbeat',
      message: '440#010101010101',
      endpoint: 'cmd',
      sid: "440",
      msg_type: "01",
      data: "0101010101"
    }, {
      label: 'Start',
      message: '00#0000',// TODO add this
      endpoint: 'cmd',
      sid: "440",
      msg_type: "16",
      data: "03"
    },
    {
      label: 'Stop',
      message: '00#0000',// TODO add this
      endpoint: 'cmd',
      sid: "440",
      msg_type: "16",
      data: "1606"
    }];

    $scope.modules = [
        {name: 'NONE',mask:'FFF'},
        {name: 'VNM', mask: '001'},
        {name: 'VSM', mask: '002'},
        {name: 'BCM', mask: '004'},
        {name: 'MCM', mask: '008'},
        {name: 'WCM', mask: '010'},
        {name: 'BMS', mask: '020'},
        {name: 'ALL', mask: '400'}
    ];

    $scope.msgType = 0;
    $scope.msgDataSize = 0;

    //Template Messages
    $scope.selectedTemplate = $scope.templates[0];
    //Custom Messages
    $scope.selectedType = $scope.msgTypes[0];
    $scope.customData = null;
    $scope.toModule = null // update this to work for more to modules []
    $scope.fromModule = null;
    //Raw Messages
    $scope.rawMessage = '';
    $scope.custMsgType = 'Template';

    //Tables
    $scope.sentMessages = [];
    $scope.messages = [];
    $scope.sortType = 'module';
    $scope.sortReverse = false;
    $scope.messageSearch = '';
    $scope.tableParams = new NgTableParams({}, { dataset: $scope.messages});

    
    $scope.sendMessage = function() {
        var endpoint
        var message
        if ($scope.custMsgType == 'Template'){
            endpoint = $scope.selectedTemplate.endpoint
            message = $scope.selectedTemplate.message
            $scope.sentMessages.push({timestamp: new Date().getTime(),
                                      sid: $scope.selectedTemplate.sid,
                                      type: $scope.selectedTemplate.label ,
                                      data: $scope.selectedTemplate.data })
        }
        else if ($scope.custMsgType == 'Custom'){
            console.log($scope.selectedType)
                endpoint = 'cmd'
                //TODO implement SID generator
                var data = $scope.customData
                if ($scope.selectedType.name == 'ENTER_STATE'){
                    data = $scope.customData.value
                }
                message = $scope.custSid+"#"+ $scope.selectedType.hex + data
                console.log("Custom message to be sent: " + message)
                $scope.sentMessages.push({timestamp: new Date().getTime(),
                                          sid: $scope.custSid,
                                          type: $scope.selectedType.label ,
                                          data: $scope.selectedType.label })
        }
        else if ($scope.custMsgType == 'Raw'){
            console.log("raw messages are not recorded in sent table")
            message = $scope.rawMessage
            endpoint = 'cmd'
        }
        $riffle.publish(endpoint,message)
        console.log("Sent message: " + message)
    }

    $scope.toggleCustMsgType = function(type){
        $scope.custMsgType = type;
    }

    $scope.updateSID = function(){
        $scope.custSid = 0;
        var to_mask = 0
        var from_mask = 0
        if ($scope.toModule){
            to_mask = $scope.parser.SID[$scope.toModule.name].to
        }
        if ($scope.fromModule){
            from_mask = $scope.parser.SID[$scope.fromModule.name].from
        }
        var ored_masks =  to_mask | from_mask
        $scope.custSid = ored_masks.toString(16)
        // for (var i<)
        // for (var i = 0; i<(3-$scope.custSid.length); i++){
        $scope.custSid = Array(4-$scope.custSid.length).join("0")+ $scope.custSid
        // }
        console.log($scope.custSid)
    }

/////////////Telemetry////////////////////////
    var chart = nv.models.bulletChart();
    $scope.progress = [];

    //Guage options
    $scope.valueFontColor = 'red';
    $scope.hideValue = false;
    $scope.hideMinMax = false;
    $scope.hideInnerShadow = false;
    $scope.gaugeWidthScale = 0.3;
    $scope.gaugeColor = 'grey';
    $scope.showInnerShadow = true;
    $scope.shadowOpacity = 0.5;
    $scope.shadowSize = 3;
    $scope.shadowVerticalOffset = 10;
    $scope.level_colors = ['#00FF00', '#FFFF00', '#FF0000'];
    $scope.hb_gauge_custom_sectors = [
        {
            color: "#00ff00",
            lo: 0,
            hi: 2000
        },
        {
            color: "#ffff00",
            lo: 2000,
            hi: 5000
        },
        {
            color: "#ff0000",
            lo: 5000,
            hi: 7000
        }
    ];
    $scope.status_bar_options = {
            chart: {
                type: 'bulletChart',
                transitionDuration: 500
            }
    };
    $scope.VNM_posX = {}
    $scope.status_bar_data = {
            "title": "Progress",
            "subtitle": "Distance m",
            "ranges": [548.64,701.04,1609,1700],
            "measures": [($scope.VNM_posX.val || 0)], //Get exact distances for each phase
            "markers": [548.64,701.04,1609,1700]
    };

    $scope.noGradient = false;
    $scope.labelFontColor = 'green';
    $scope.startAnimationTime = 0;
    $scope.donut = undefined;
    $scope.donutAngle = 90;
    $scope.counter = true;
    $scope.decimals = 2;
    $scope.symbol = 'X';
    $scope.formatNumber = true;
    $scope.humanFriendly = true;
    $scope.humanFriendlyDecimal = true;
    $scope.textRenderer = function (value) {
        return value;
    };

//////////////////////////MCM////////////////////////////
$scope.MCM_linegraph_options = {
            chart: {
                type: 'lineChart',
                height: 200,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 60,
                    left: 65
                },
                // forceY:[0,7000],
                x: function(d){ return d[0]; },
                y: function(d){ return d[1]; },
                //average: function(d) { return d.mean/100; },

                color: d3.scale.category10().range(),
                duration: 300,
                useInteractiveGuideline: true,
                clipVoronoi: false,

                xAxis: {
                    axisLabel: 'X Axis',
                    tickFormat: function(d) {
                        return d3.time.format('%m/%d/%y')(new Date(d))
                    },
                    showMaxMin: false,
                    staggerLabels: true
                },

                // yAxis: {
                //     axisLabel: 'Y Axis',
                //     // tickFormat: function(d){
                //     //     return d3.format('.01f')(d);
                //     //     //return d3.format(',.1%')(d);
                //     // },
                //     axisLabelDistance: 20
                // }
            }
        };

$scope.MCM_linegraph_data = [
            {
                key: "Wheel 1",
                values: []
                //mean: 250
            },
            {
                key: "Wheel 2",
                values: []
                //mean: -60
            },

            {
                key: "Wheel 3",
                //mean: 125,
                values: [] 
            },
            {
                key: "Wheel 4",
                values: [] 
            }
        ];
$scope.BCM_linegraph_data = [
            {
                key: "Brake 1",
                values: []
                //mean: 250
            },
            {
                key: "Brake 2",
                values: []
                //mean: -60
            },

            {
                key: "Brake 3",
                //mean: 125,
                values: [] 
            },
            {
                key: "Brake 4",
                values: [] 
            }
        ];
    var x = new Date().getTime();
    var update_chart_values = function(){
        $scope.status_bar_data.measures = [($scope.VNM_posX.val || 0)]
        $scope.VSM_barchart_data = [
            {
                key: "Temperatures",
                values: [
                    {
                        "label" : "HV1" ,
                        "value" : $scope.VSM_T_HV1.val || 0

                    } ,
                    {
                        "label" : "HV2" ,
                        "value" : $scope.VSM_T_HV2.val || 0
                    } ,
                    {
                        "label" : "Motor1" ,
                        "value" : $scope.VSM_T_motor1.val || 0
                    } ,
                    {
                        "label" : "Motor2" ,
                        "value" : $scope.VSM_T_motor2.val || 0
                    } ,
                    {
                        "label" : "Motor3" ,
                        "value" : $scope.VSM_T_motor3.val || 0
                    } ,
                    {
                        "label" : "Motor4" ,
                        "value" : $scope.VSM_T_motor4.val || 0
                    } ,
                    {
                        "label" : "WCM1" ,
                        "value" : $scope.VSM_T_WCM1.val || 0
                    } ,
                    {
                        "label" : "WCM2" ,
                        "value" : $scope.VSM_T_WCM2.val || 0
                    },
                    {
                        "label" : "Cabin" ,
                        "value" : $scope.VSM_T_cabin.val || 0
                    },
                    {
                        "label" : "12V1" ,
                        "value" : $scope.VSM_T_12V1.val || 0
                    },
                    {
                        "label" : "12V2" ,
                        "value" : $scope.VSM_T_12V2.val || 0
                    }
                ]
            }
        ]
        x = new Date().getTime();
        // Add MCM Wheel RPM speed
        $scope.MCM_linegraph_data[0].values.push([x,$scope.MCM_HB1_spd.val]);
        $scope.MCM_linegraph_data[1].values.push([x,$scope.MCM_HB2_spd.val]);
        $scope.MCM_linegraph_data[2].values.push([x,$scope.MCM_HB3_spd.val]);
        $scope.MCM_linegraph_data[3].values.push([x,$scope.MCM_HB4_spd.val]);
        //Conserve memory by shifting out old data
        if ($scope.MCM_linegraph_data[0].values.length > 20){
            $scope.MCM_linegraph_data[0].values.shift();
        }
        if ($scope.MCM_linegraph_data[1].values.length > 20){
            $scope.MCM_linegraph_data[1].values.shift();
        }
        if ($scope.MCM_linegraph_data[2].values.length > 20){
            $scope.MCM_linegraph_data[2].values.shift();
        }
        if ($scope.MCM_linegraph_data[3].values.length > 20){
            $scope.MCM_linegraph_data[3].values.shift();
        }

        // Add BCM Wheel RPM speed
        $scope.BCM_linegraph_data[0].values.push([x,$scope.BCM_Brake_1_spd.val]);
        $scope.BCM_linegraph_data[1].values.push([x,$scope.BCM_Brake_2_spd.val]);
        $scope.BCM_linegraph_data[2].values.push([x,$scope.BCM_Brake_3_spd.val]);
        $scope.BCM_linegraph_data[3].values.push([x,$scope.BCM_Brake_4_spd.val]);
        //Conserve memory by shifting out old data
        if ($scope.BCM_linegraph_data[0].values.length > 20){
            $scope.BCM_linegraph_data[0].values.shift();
        }
        if ($scope.BCM_linegraph_data[1].values.length > 20){
            $scope.BCM_linegraph_data[1].values.shift();
        }
        if ($scope.BCM_linegraph_data[2].values.length > 20){
            $scope.BCM_linegraph_data[2].values.shift();
        }
        if ($scope.BCM_linegraph_data[3].values.length > 20){
            $scope.BCM_linegraph_data[3].values.shift();
        }
    }
    setInterval(function(){
        update_chart_values()
    }, 500);

//////////////////////////VSM////////////////////////////

        $scope.VSM_T_HV1 = {}
        $scope.VSM_T_HV2 = {}
        $scope.VSM_T_motor1 = {}
        $scope.VSM_T_motor2 = {}
        $scope.VSM_T_motor3 = {}
        $scope.VSM_T_motor4 = {}
        $scope.VSM_T_WCM1 = {}
        $scope.VSM_T_WCM2 = {}
        $scope.VSM_T_cabin = {}
        $scope.VSM_T_12V1 = {}
        $scope.VSM_T_12V2 = {}

        //Temperature bar chart
        $scope.VSM_barchart_options = {
            chart: {
                type: 'discreteBarChart',
                height: 350,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 50,
                    left: 55
                },
                color: function (d, i) {
                    if (d.value < 100){
                        return "#00FF00"
                    }
                    else if (d.value >= 100 && d.value < 150){
                        return "#FFFF00"
                    }
                    else if (d.value >= 150){
                        return "#FF0000"
                    }
                },
                x: function(d){return d.label;},
                y: function(d){return d.value + (1e-10);},
                showValues: true,
                valueFormat: function(d){
                    return d3.format(',.4f')(d);
                },
                forceY: [0,150],
                duration: 500,
                xAxis: {
                    axisLabel: ''
                },
                yAxis: {
                    axisLabel: 'Temperature  C',
                    axisLabelDistance: -10
                }
            }
        };

        //Hacky JS thing to get the chart to work

        $scope.VSM_barchart_data = [
            {
                key: "Temperatures",
                values: [
                    {
                        "label" : "HV1" ,
                        "value" : $scope.VSM_T_HV1.val || 0

                    } ,
                    {
                        "label" : "HV2" ,
                        "value" : $scope.VSM_T_HV2.val || 0
                    } ,
                    {
                        "label" : "Motor1" ,
                        "value" : $scope.VSM_T_motor1.val || 0
                    } ,
                    {
                        "label" : "Motor2" ,
                        "value" : $scope.VSM_T_motor2.val || 0
                    } ,
                    {
                        "label" : "Motor3" ,
                        "value" : $scope.VSM_T_motor3.val || 0
                    } ,
                    {
                        "label" : "Motor4" ,
                        "value" : $scope.VSM_T_motor4.val || 0
                    } ,
                    {
                        "label" : "WCM1" ,
                        "value" : $scope.VSM_T_WCM1.val || 0
                    } ,
                    {
                        "label" : "WCM2" ,
                        "value" : $scope.VSM_T_WCM2.val || 0
                    },
                    {
                        "label" : "Cabin" ,
                        "value" : $scope.VSM_T_cabin.val || 0
                    },
                    {
                        "label" : "12V1" ,
                        "value" : $scope.VSM_T_12V1.val || 0
                    },
                    {
                        "label" : "12V2" ,
                        "value" : $scope.VSM_T_12V2.val || 0
                    }
                    
                ]
            }
        ]



$scope.get_status = function(val, max, min){
    // TODO: Add logic for binary values
    var warn_max = max - (max * 0.1) // 10% of max do we want to warn?
    var warn_min = min + (max * 0.1) // 10% of max do we want to warn?

    var types = ['success', 'info', 'warning', 'danger'];

    if (val > max || val < min){
        return 'danger'
    }
    else if (val >= warn_max || val <= warn_min){
        return 'warning'
    }
    else if (val <= max && val >= min){
        return 'success'
    }
    else{
        return 'info'
    }
}

//Don't think we need this
// $scope.get_progress = function() {
//     $scope.stacked = [];
//     var types = ['success', 'info', 'warning', 'danger'];

//     for (var i = 0, n = Math.floor(Math.random() * 4 + 1); i < n; i++) {
//         var index = Math.floor(Math.random() * 4);
//         $scope.progress.push({
//           value: Math.floor(Math.random() * 30 + 1),
//           type: types[index]
//         });
//     }
//   };

// $scope.get_progress();



var add_message_to_array = function(timestamp,sid,type,data){
    if ($scope.messages.length > 30){ //Limit number of messages in array to conserve memory
        $scope.messages.shift();
    }
    // var timestamp = new Date(parseFloat(msg[0]))
    // var sid = msg[1]
    // var type = msg[2]
    // msg.splice(0,3)
    // console.log(msg)
    $scope.messages.push({
                            timestamp: timestamp,
                            sid:sid,
                            type:type,
                            data:msg
                        })
}

$riffle.subscribe("data", function(data) {
    console.log("got parsed data")
    //Data will be in the format [[timestamp, sid, message type, data]]
    //console.log(data)
    for (var i = 0; i<data.length; i++){
        // console.log(data[i][0])
        // console.log(data[i][1])
        var title = data[i][0]
        var max = $scope[title].max
        var min = $scope[title].min

        $scope[data[i][0]].val = data[i][1]
        $scope[title].status_style = $scope.get_status($scope[title].val,max,min)
    }
    //$scope.$apply()
});

$riffle.subscribe("hb", function(data) {
    var modules = Object.keys(data['modules'])
    for (var f = 0; f<modules.length; f++){
        //console.log(modules[f])
        $scope[modules[f]] = data['modules'][modules[f]]

    }
    $scope['system_status'] = data['system_status']
});

$riffle.subscribe("can", function(data) {
    console.log("got can data")
    //Data will be in the format [[timestamp, sid, message type, data]]
    //console.log(data)
    for (var i = 0; i<data.length; i++){
        add_message_to_array(data[i][0],data[i][1],data[i][2],data[i][3])
    }
});

//////////////////////////GUAGE CONGFIGURAION///////////////////////////
    $scope.upperLimit = 25;
    $scope.lowerLimit = -25;
    $scope.unit = "";
    $scope.precision = 2;
    $scope.roll_ranges = [
        {
            min: -25,
            max: -10,
            color: '#FF0000'
        },
        {
            min: -10,
            max: -2,
            color: '#FFFF00'
        },
        {
            min: -2,
            max: 2,
            color: '#00FF00'
        },
        {
            min: 2,
            max: 10,
            color: '#FFFF00'
        },
        {
            min: 10,
            max: 25,
            color: '#FF0000'
        }
    ];
    $scope.yaw_ranges = [
        {
            min: -25,
            max: -5,
            color: '#FF0000'
        },
        {
            min: -5,
            max: -2,
            color: '#FFFF00'
        },
        {
            min: -2,
            max: 2,
            color: '#00FF00'
        },
        {
            min: 2,
            max: 5,
            color: '#FFFF00'
        },
        {
            min: 5,
            max: 25,
            color: '#FF0000'
        }
    ];
    $scope.pitch_ranges = [
        {
            min: -25,
            max: -4,
            color: '#FF0000'
        },
        {
            min: -4,
            max: -2,
            color: '#FFFF00'
        },
        {
            min: -2,
            max: 2,
            color: '#00FF00'
        },
        {
            min: 2,
            max: 4,
            color: '#FFFF00'
        },
        {
            min: 4,
            max: 25,
            color: '#FF0000'
        }
    ];

//////////////////////////GRAPH CONGFIGURAION///////////////////////////
  	 $scope.options = {
            chart: {
                type: 'lineChart',
                height: 450,
                margin : {
                    top: 20,
                    right: 20,
                    bottom: 40,
                    left: 55
                },
                x: function(d){ return d.x; },
                y: function(d){ return d.y; },
                useInteractiveGuideline: true,
                dispatch: {
                    stateChange: function(e){ console.log("stateChange"); },
                    changeState: function(e){ console.log("changeState"); },
                    tooltipShow: function(e){ console.log("tooltipShow"); },
                    tooltipHide: function(e){ console.log("tooltipHide"); }
                },
                xAxis: {
                    axisLabel: 'Time (ms)'
                },
                yAxis: {
                    axisLabel: 'Voltage (v)',
                    tickFormat: function(d){
                        return d3.format('.02f')(d);
                    },
                    axisLabelDistance: -10
                },
                callback: function(chart){
                    console.log("!!! lineChart callback !!!");
                }
            },
            title: {
                enable: true,
                text: 'Velocity and Acceleration'
            },
            subtitle: {
                enable: true,
                text: 'Velocity and Acceleration',
                css: {
                    'text-align': 'center',
                    'margin': '10px 13px 0px 7px'
                }
            },
            caption: {
                enable: false,
               	text: 'Velocity and Accelleration of the BadgerLoop Pod',
                css: {
                    'text-align': 'justify',
                    'margin': '10px 13px 0px 7px'
                }
            }
        };

    //The function that spams data
    // setInterval(function(){
    //     //Update line chart
    //     // if (!$scope.run) return;
    //     var parser_keys = Object.keys($scope.parser.msg_type)
    //     for (var k in $scope.parser.msg_type){
    //         var mesage_obj = $scope.parser.msg_type[k]
    //         if (!mesage_obj.cmd){
    //             for (var g = 0; g<mesage_obj.values.length; g++){

                
    //                 var scope_var_key = Object.keys(mesage_obj.values[g])[0]
    //                 //console.log(scope_var_key)
    //                 var max = $scope[scope_var_key].max
    //                 var max = max + (max*.05)
    //                 var min = $scope[scope_var_key].min
    //                 var min = min - (max*.05)
    //                 var offset = Math.floor(max * .1)
    //                 $scope[scope_var_key].val = Math.floor(Math.random() * (max - min) + min);
    //                 $scope[scope_var_key].status_style = $scope.get_status($scope[scope_var_key].val,$scope[scope_var_key].max,$scope[scope_var_key].min);
    //                 //console.log($scope[scope_var_key].status_style)
    //                 //console.log($scope.VNM_posX.val)
    //                 //$scope.d3_api.refresh();
    //             }
    //         }
    //     }
    //     // for(var b = 0; b<parser_keys.length; b++){
    //     //     message = parser_keys
    //     //     for(var c = 0 c<parser_keys){

    //     //     }
    //     // }
    //    update_chart_values();
    //    $scope.$apply(); // update both chart
    //    // $scope.d3_api.refresh();
    // }, 500);
  });
