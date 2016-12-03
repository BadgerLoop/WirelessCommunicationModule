package main

import "time"
import "github.com/exis-io/core"
import "github.com/exis-io/core/riffle"
import "math/rand"

var sender riffle.Domain
var receiver riffle.Domain

func connect(){

	core.LogLevel = core.LogLevelDebug
	// Create a domain
	riffle.SetFabric("ws://192.168.1.99:8000")
	// Create the domain objects
	app := riffle.NewDomain("xs")
	//receiver := app.Subdomain("cmd")
	sender = app.Subdomain("node")
	//sender.Join()
	//return sender
}

func main() {

	
		// Super hack - sleep to let the connection come up
		//var ep string

		connect()
		sender.Join()
		ep := "exis"
		var m = make(map[string]int)
		time.Sleep(200 * time.Millisecond)
		m["mcm_prog"] = 0
		m["bcm_prog"] = 0
		m["vsm_prog"] = 0
		m["vnm_prog"] = 0
		m["lw1_rpm"] = 0
		m["lw2_rpm"] = 0
		m["rw1_rpm"] = 0
		m["rw2_rpm"] = 0
		m["lw1_tmp"] = 0
		m["lw2_tmp"] = 0
		m["rw1_tmp"] = 0
		m["rw2_tmp"] = 0

	for m["mcm_prog"] < 100 || m["bcm_prog"] < 100 || m["vsm_prog"] < 100 || m["vnm_prog"] < 100 {

		m["mcm_prog"] = m["mcm_prog"] + rand.Intn(4)
		m["bcm_prog"] = m["bcm_prog"] + rand.Intn(4)
		m["vsm_prog"] = m["vsm_prog"] + rand.Intn(4)
		m["vnm_prog"] = m["vnm_prog"] + rand.Intn(4)

		sender.Publish(ep, m)
		time.Sleep(120 * time.Millisecond)
	}
		m["mcm_prog"] = 100
		m["bcm_prog"] = 100
		m["vsm_prog"] = 100
		m["vnm_prog"] = 100

	var  w_range_l int = 0;
	var  w_range_offset int = 10;
	var  t_range_l int = 0;
	var  t_range_offset int = 4;
	var  decrease int = 0;
	var  count int = 0;
	for {
			m["lw1_rpm"] = w_range_l + rand.Intn(w_range_offset)
			m["lw2_rpm"] = w_range_l + rand.Intn(w_range_offset)
			m["rw1_rpm"] = w_range_l + rand.Intn(w_range_offset)
			m["rw2_rpm"] = w_range_l + rand.Intn(w_range_offset)
			m["lw1_tmp"] = t_range_l + rand.Intn(t_range_offset)
			m["lw2_tmp"] = t_range_l + rand.Intn(t_range_offset)
			m["rw1_tmp"] = t_range_l + rand.Intn(t_range_offset)
			m["rw2_tmp"] = t_range_l + rand.Intn(t_range_offset)
			// velocity range
			if m["velocity"] >= 200 {
				m["velocity"] = 200 + rand.Intn(20)
			} else {
				m["velocity"] = m["velocity"] + rand.Intn(4)
			}
			// Temp range
			if t_range_l >= 90 {
				t_range_l = t_range_l
			} else {
				t_range_l = t_range_l + rand.Intn(3)
			}

			//Wheel speed range
			if w_range_l >= 5000 || decrease == 1 {
				if count > 100 {
					decrease = 1
					w_range_l = w_range_l - 100;
				} else { 
					count = count + 1
				}
			} else {
				w_range_l = w_range_l + 100
			}
			
			// Make the call to get the data we need
			//core.Info("Sending %v, %v", ep, ret)
			time.Sleep(120 * time.Millisecond)

			//Failover if lost websocket connection
			defer func(){main()}()
			sender.Publish(ep, m)
	}
	//sender.Listen()

}
