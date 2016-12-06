package main

import "time"
import "github.com/exis-io/core/riffle"


func main() {
        riffle.SetLogLevelInfo()
        // Create a domain
        riffle.SetFabric("ws://192.168.1.99:8000")
        cmd := "stop"
        // Create the domain objects
        app := riffle.NewDomain("xs")
        sender := app.Subdomain("node")

        sender.Join()
        time.Sleep(200 * time.Millisecond)
        sender.Publish("cmd", cmd)
        time.Sleep(200 * time.Millisecond)
        sender.Publish("stop", cmd)
}
