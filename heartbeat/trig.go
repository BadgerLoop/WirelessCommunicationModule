package main

import "time"
import "github.com/exis-io/core/riffle"


func main() {
        riffle.SetLogLevelInfo()
        // Create a domain
        riffle.SetFabric("ws://192.168.1.99:9000")
        // Create the domain objects
        app := riffle.NewDomain("xs")
        sender := app.Subdomain("node")

        sender.Join()
        // time.Sleep(200 * time.Millisecond)
        // sender.Publish("hb_ctrl", [3]int{0,100,100})
        // time.Sleep(200 * time.Millisecond)
        // sender.Publish("hb_ctrl", [3]int{0,100,100})
        // time.Sleep(200 * time.Millisecond)


        sender.Publish("can", [3]int{1,100,100})
        time.Sleep(200 * time.Millisecond)
        sender.Publish("can", [3]int{1,100,100})
}
