package validator

import (
	"time"
)
var Hb_send = false
var Interval_ms = 0
var FaultCount = 0
var FaultMax = 0
var StartTime = time.Now().UnixNano()%1e6/1e3
var Rx_hb_empty = true
var	Rx_hb = map[string]string{
    		"01": "",
    		"02": "",
    		"03": "",
    		"04": "",
    		"19": "",
		}
var EndTime = time.Now().UnixNano()%1e6/1e3