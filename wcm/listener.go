
package main

import (
	// "fmt"
	//"time"
    "os/exec"
	riffle "github.com/exis-io/core/riffle"
)

func listen(sender riffle.Domain){
		for {
			// Make the call to get the data we need
			//if out, err := exec.Command("python3","listen.py","can0").Output(); err != nil {
			if out, err := exec.Command("candump","can0").Output(); err != nil {
				riffle.Error("Error %v", err)
			} else {
				str := string(out)
				//if ep, pyld, err := parse(str); err == nil {
					riffle.Info("Sending %s", out)
					sender.Publish("can", str)
				}
			//}
				//time.Sleep(3 * time.Second)
		}
}

func cmd(command string) {
	riffle.Info("Command received: %s", command)
}

func hb(heartbeat string) {
	riffle.Info("Heartbeat received: %s", heartbeat)
}

func main() {
	// set flags for testing
	//riffle.SetFabricLocal()
	riffle.SetLogLevelInfo()
	riffle.SetFabric("ws://192.168.1.99:9000")
	// Domain objects
	app := riffle.NewDomain("xs.node")

	heartbeat := app.Subdomain("hb")
	sender := app.Subdomain("can")
	receiver := app.Subdomain("cmd")
	// Connect
	//receiver.SetToken("1o1-sPF0NWy2kWcv0XHJxpVUkMHWblQrfa5-cVXcsMujjl-l3W2CNgFSR.1LIE6S-QNT31RCLWgRBvFyGFy0BznBOzvdS8Xr0z9i4iatUWDOV1EdH4PtVd4RDMA5yVr3Ioz2cdvHmWas4rA3plr8G-XiCCjzF7NYE-YYRiaOmZ0_")
	receiver.Join()
	heartbeat.Join()
	sender.Join()

	if e := receiver.Subscribe("cmd", cmd); e != nil {
		riffle.Info("Unable to subscribe: to cmd endpoint", e.Error())
	} else {
		riffle.Info("Subscribed to cmd endpoint!")
	}

	if e := heartbeat.Subscribe("hb", hb); e != nil {
		riffle.Info("Unable to subscribe to heartbeat endpoint ", e.Error())
	} else {
		riffle.Info("Subscribed to heartbeat!")
	}

	go listen(sender)

	// Handle until the connection closes
	heartbeat.Listen()
	receiver.Listen()
}