
package main

import (
	"fmt"
	"time"
	"strings"
    "os/exec"
	riffle "github.com/exis-io/core/riffle"
)

func parse(str string) []string{
	//TODO: This may be able to be optimized also need to handle errors
	//Split output from candump
	pstring := strings.Split(str, "  ")
	if len(pstring) < 4 || len(pdata[1])<2{
		return nil
	}
	//Split data segment to get message type
	pdata := strings.SplitN(pstring[4], " ", 2)
	//[timestamp,sid,type,data]
	return []string{time.Now().String(),pstring[2],pdata[0],pdata[1]}
}

func parse_batch(str string) [][]string{
	fmt.Printf(str)
	message_list := strings.Split(str, "\n")
	batch := [][]string{}
	for i, _ := range message_list {
		parsed_message := parse(message_list[i])
		if parsed_message != nil {
    		batch = append(batch,parsed_message)
    	}
	}
	return batch
}

func listen_can(app riffle.Domain){
		//Heartbeat message ids
		// is_hb := map[string]bool{
  //   		"01": true,
  //   		"02": true,
  //   		"03": true,
  //   		"04": true,
  //   		"19": true,
		// }
		for {
			// Make the call to get the data we need
			//if out, err := exec.Command("python3","listen.py","can0").Output(); err != nil {
			if out, err := exec.Command("candump","-n","10","can1").Output(); err != nil {
				riffle.Error("Error %v", err)
			} else {
				str := string(out)
				fmt.Printf(str)
				send_data := parse_batch(str)

				riffle.Info("Sending %s", send_data)

				app.Publish("can", send_data)
				//TODO: add hb validator logic
				// if (is_hb[send_data[2]]){
				// 	app.Publish("hb", send_data)
				// }
			}
		//time.Sleep(5 * time.Second)
		}
}

func cmd(command string) {
	riffle.Info("Command received: %s", command)
	if _, err := exec.Command("cansend","can1",command).Output(); err != nil {
		riffle.Error("Error %v", err)
	} else {
		riffle.Info("Sent command to CAN: %s", command)
	}
}

func hb(heartbeat []string) {
	riffle.Info("Heartbeat from nuc received: %s", heartbeat)

}

func listen(app riffle.Domain){
        app.Listen()
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

	go listen_can(app)

	// Handle until the connection closes
	listen(app)
	//If connection closed reopen
    defer func(){listen(app)}()
}