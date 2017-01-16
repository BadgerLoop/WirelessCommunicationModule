
package main

import (
	"fmt"
	//"time"
	"strings"
    "os/exec"
	riffle "github.com/exis-io/core/riffle"
)

func listen(app riffle.Domain){
		for {
			// Make the call to get the data we need
			//if out, err := exec.Command("python3","listen.py","can0").Output(); err != nil {
			if out, err := exec.Command("candump","-n","1","can1").Output(); err != nil {
				riffle.Error("Error %v", err)
			} else {
				str := string(out)
				//TODO: This may be able to be optimized also need to handle errors
				//Split output from candump
				pstring := strings.Split(str, "  ")
				//Split data segment to get message type
				pdata := strings.SplitN(pstring[4], " ", 2)
				send_data := string[4]{time.Now().String(),pstring[2],pdata[0],p2data[1]}
				riffle.Info("Sending %s", send_data)
				app.Publish("can", send_data)
			}
		//time.Sleep(5 * time.Second)
		}
}

func cmd(command string) {
	riffle.Info("Command received: %s", command)
	if out, err := exec.Command("cansend","can1",command).Output(); err != nil {
		riffle.Error("Error %v", err)
	} else {
		riffle.Info("Sent command to CAN: %s", command)
	}
}

func hb(heartbeat string) {
	riffle.Info("Heartbeat received: %s", heartbeat)
	if out, err := exec.Command("cansend","can1",heartbeat).Output(); err != nil {
		riffle.Error("Error %v", err)
	} else {
		riffle.Info("Sent heartbeat to CAN: %s", heartbeat)
	}
}

func main() {
	// set flags for testing
	//riffle.SetFabricLocal()
	riffle.SetLogLevelInfo()
	riffle.SetFabric("ws://192.168.1.99:9000")
	// Domain objects
	core := riffle.NewDomain("xs")
	app := core.Subdomain("node")
	// heartbeat := app.Subdomain("hb")
	// sender := app.Subdomain("can")
	// receiver := app.Subdomain("cmd")
	// Connect
	app.Join()
	// heartbeat.Join()
	// sender.Join()

	// if e := receiver.Subscribe("cmd", cmd); e != nil {
	if e := app.Subscribe("cmd", cmd); e != nil {
		riffle.Info("Unable to subscribe to cmd endpoint", e.Error())
	} else {
		riffle.Info("Subscribed to cmd endpoint!")
	}

	// if e := heartbeat.Subscribe("hb", hb); e != nil {
	if e := app.Subscribe("cmd", cmd); e != nil {
		riffle.Info("Unable to subscribe to heartbeat endpoint ", e.Error())
	} else {
		riffle.Info("Subscribed to heartbeat!")
	}

	go listen(app)
	// Handle until the connection closes
	app.Listen()
	// receiver.Listen()
}