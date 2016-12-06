package main

import "time"
//import "github.com/exis-io/core"
import "github.com/exis-io/core/riffle"
import "math/rand"
import "fmt"


var sender riffle.Domain
var m = make(map[string]int)

var rpm_max int = 5000
var temp_max int = 90
var temp_min int = 20
var velocity_max int = 200

var  t_range_offset int = 4
var  w_range_offset int = 100;
var  v_range_offset int = 3;

var  coast_count int = 100;

func connect(){
	//Use if we want to print debug messages
	//core.LogLevel = core.LogLevelDebug 

	riffle.SetFabric("ws://192.168.1.99:8000")

	// Create the domain objects
	app := riffle.NewDomain("xs")
	sender = app.Subdomain("node")
	sender.Join()
}


func initialize(){
	
		m["mcm_prog"] = 0
		m["bcm_prog"] = 0
		m["vsm_prog"] = 0
		m["vnm_prog"] = 0
		m["node1_prog"] = 0
		m["node2_prog"] = 0
		m["node3_prog"] = 0
		m["node4_prog"] = 0

	fmt.Printf("Initializing nodes...\n")
	for (m["node1_prog"] < 100 || m["node2_prog"] < 100 || m["node3_prog"] < 100 || m["node4_prog"] < 100) {
		m["node1_prog"] = m["node1_prog"] + rand.Intn(4)
		m["node2_prog"] = m["node2_prog"] + rand.Intn(4)
		m["node3_prog"] = m["node3_prog"] + rand.Intn(4)
		m["node4_prog"] = m["node4_prog"] + rand.Intn(4)
		sender.Publish("exis", m)
		time.Sleep(80 * time.Millisecond)
	}
		m["node1_prog"] = 100
		m["node2_prog"] = 100
		m["node3_prog"] = 100
		m["node4_prog"] = 100
		sender.Publish("exis", m)

	fmt.Printf("Initializing modules...\n")
	for (m["mcm_prog"] < 100 || m["bcm_prog"] < 100 || m["vsm_prog"] < 100 || m["vnm_prog"] < 100) {
		m["mcm_prog"] = m["mcm_prog"] + rand.Intn(4)
		m["bcm_prog"] = m["bcm_prog"] + rand.Intn(4)
		m["vsm_prog"] = m["vsm_prog"] + rand.Intn(4)
		m["vnm_prog"] = m["vnm_prog"] + rand.Intn(4)
		sender.Publish("exis", m)
		time.Sleep(80 * time.Millisecond)
	}
		m["mcm_prog"] = 100
		m["bcm_prog"] = 100
		m["vsm_prog"] = 100
		m["vnm_prog"] = 100
		sender.Publish("exis", m)
	fmt.Printf("Initialization complete...\n")
}


func speed_up(){

		fmt.Printf("Accellerating... \n")
		for m["velocity"] < velocity_max {
			m["lw1_rpm"] = (m["velocity"] * 20) + rand.Intn(w_range_offset)
			m["lw2_rpm"] = (m["velocity"] * 20) + rand.Intn(w_range_offset)
			m["rw1_rpm"] = (m["velocity"] * 20) + rand.Intn(w_range_offset)
			m["rw2_rpm"] = (m["velocity"] * 20) + rand.Intn(w_range_offset)
			
			m["lw1_tmp"] = temp_min + m["velocity"]/3 + rand.Intn(t_range_offset)
			m["lw2_tmp"] = temp_min + m["velocity"]/3 + rand.Intn(t_range_offset)
			m["rw1_tmp"] = temp_min + m["velocity"]/3 + rand.Intn(t_range_offset)
			m["rw2_tmp"] = temp_min + m["velocity"]/3 + rand.Intn(t_range_offset)

			m["velocity"] = m["velocity"] + rand.Intn(v_range_offset) + 2
			m["accel_prog"] = m["velocity"]/3

		time.Sleep(120 * time.Millisecond)
		sender.Publish("exis", m)
	}
	time.Sleep(120 * time.Millisecond)
}

func coast(){

	fmt.Printf("Coasting... \n")
	var count int = 0;
	for count < coast_count {
			
			m["lw1_rpm"] = rpm_max + rand.Intn(w_range_offset)
			m["lw2_rpm"] = rpm_max + rand.Intn(w_range_offset)
			m["rw1_rpm"] = rpm_max  + rand.Intn(w_range_offset)
			m["rw2_rpm"] = rpm_max  + rand.Intn(w_range_offset)

			m["lw1_tmp"] = temp_max + rand.Intn(t_range_offset)
			m["lw2_tmp"] = temp_max + rand.Intn(t_range_offset)
			m["rw1_tmp"] = temp_max + rand.Intn(t_range_offset)
			m["rw2_tmp"] = temp_max + rand.Intn(t_range_offset)

			m["velocity"] = velocity_max + rand.Intn(v_range_offset)
			m["coast_prog"] = count/6 + 1// Hacky
		
			time.Sleep(120 * time.Millisecond)
			sender.Publish("exis", m)
		count = count+1
	}
	time.Sleep(120 * time.Millisecond)
}

func slow_down(){
	
	fmt.Printf("Braking... \n")
	for m["velocity"]>v_range_offset {

		m["lw1_rpm"] = (m["velocity"] * 20) + rand.Intn(w_range_offset)
		m["lw2_rpm"] = (m["velocity"] * 20) + rand.Intn(w_range_offset)
		m["rw1_rpm"] = (m["velocity"] * 20) + rand.Intn(w_range_offset)
		m["rw2_rpm"] = (m["velocity"] * 20) + rand.Intn(w_range_offset)

		m["lw1_tmp"] = temp_min + m["velocity"]/3 + rand.Intn(t_range_offset)
		m["lw2_tmp"] = temp_min + m["velocity"]/3 + rand.Intn(t_range_offset)
		m["rw1_tmp"] = temp_min + m["velocity"]/3 + rand.Intn(t_range_offset)
		m["rw2_tmp"] = temp_min + m["velocity"]/3 + rand.Intn(t_range_offset)

		m["velocity"] = m["velocity"] - rand.Intn(v_range_offset) - 4
		m["slow_prog"] = 50 - (m["velocity"]/4)

		time.Sleep(120 * time.Millisecond)
		sender.Publish("exis", m)
	}

	for m["lw1_rpm"] > 0 && m["lw2_rpm"] > 0 && m["rw1_rpm"] > 0 && m["rw2_rpm"] > 0 {

		m["lw1_rpm"] = m["lw1_rpm"] - 10
		m["lw2_rpm"] = m["lw2_rpm"] - 10
		m["rw1_rpm"] = m["rw1_rpm"] - 10
		m["rw2_rpm"] = m["rw2_rpm"] - 10

		time.Sleep(120 * time.Millisecond)
		sender.Publish("exis", m)
	}

	m["lw1_rpm"] = 0
	m["lw2_rpm"] = 0
	m["rw1_rpm"] = 0
	m["rw2_rpm"] = 0

	time.Sleep(120 * time.Millisecond)
	sender.Publish("exis", m)
}

func run(){

		fmt.Printf("Starting Simulation... \n")
		//Wheel RPMs
		m["lw1_rpm"] = 0
		m["lw2_rpm"] = 0
		m["rw1_rpm"] = 0
		m["rw2_rpm"] = 0

		//Wheel Temps
		m["lw1_tmp"] = temp_min
		m["lw2_tmp"] = temp_min
		m["rw1_tmp"] = temp_min
		m["rw2_tmp"] = temp_min
		m["velocity"] = temp_min

		//Velocity
		m["velocity"] = 0

		//Progress
		m["accel_prog"] = 0
		m["coast_prog"] = 0
		m["slow_prog"] = 0

		speed_up()
		coast()
		slow_down()

		fmt.Printf("Simulation Completed... \n")
}

func main() {
		connect()
		
		sender.Subscribe("cmd", func(a string) {
			fmt.Printf("Received Command: %s \n", a)
			if a == "run" {
				run();
			} else if a == "stop" {
				//TODO: Add stop functionality
			} else if a == "init" {
				initialize();
			}
		})
		fmt.Printf("Waiting for command... \n")
		defer func(){main()}()
		sender.Listen()
}


