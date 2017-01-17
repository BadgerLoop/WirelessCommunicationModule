package main
import (
    riffle "github.com/exis-io/core/riffle"
    validator "./validator"
    "time"
)

func hb_driver(){
    c := riffle.NewDomain("xs")
    sender := c.Subdomain("node")
    sender.Join()
        for {
            if validator.Hb_send {
                sender.Publish("can", "5C0#1301") //May want to send heartbeat can message here
                riffle.Info("Sending WCM heartbeat")
                time.Sleep(time.Duration(validator.Interval_ms) * time.Millisecond)
            }
        }
}

func hb_ctrl(data []int){

        if data[0] == 1 {
            riffle.Info("received hb start command")
            validator.Hb_send = true
            validator.Interval_ms = data[1]
        } else if (data[0] == 0) {
            riffle.Info("received hb stop command")
            validator.Hb_send = false
        }
}

func hb_handler(data []string){
    

    if validator.Rx_hb_empty {
        validator.StartTime = time.Now().UnixNano()%1e6/1e3
        validator.Rx_hb_empty = false
    }

    validator.Rx_hb[data[1]] = data[2]
    full:=true

    for _, v := range validator.Rx_hb { 
        if v == ""{
            full = false
        }
    }

    if full {
        for k, _ := range validator.Rx_hb { 
            validator.Rx_hb[k] = ""
        }
        validator.EndTime = time.Now().UnixNano()%1e6/1e3
        validator.Rx_hb_empty = true
    }

    if ((validator.EndTime - validator.StartTime)>int64(validator.Interval_ms)){
        validator.FaultCount = validator.FaultCount + 1
    }else{
        validator.FaultCount = 0
    }
}

func listen(app riffle.Domain){
        app.Listen()
}

func main() {
        riffle.SetLogLevelInfo()
        // Create a domain
        riffle.SetFabric("ws://192.168.1.99:9000")
        // Create the domain objects
        core := riffle.NewDomain("xs")
        app := core.Subdomain("node")
        app.Join()

        if e := app.Subscribe("hb_ctrl", hb_ctrl); e != nil {
                riffle.Info("Unable to subscribe to hb_ctrl endpoint", e.Error())
        } else {
                riffle.Info("Subscribed to hb_ctrl endpoint!")
        }

        if e := app.Subscribe("hb", hb_handler); e != nil {
                riffle.Info("Unable to subscribe to can endpoint", e.Error())
        } else {
                riffle.Info("Subscribed to heartbeat endpoint!")
        }
        // go hb_driver()
        listen(app)
        defer func(){listen(app)}()
}