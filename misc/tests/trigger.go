package main

import "time"
import "github.com/exis-io/core/riffle"


func main() {
        riffle.SetLogLevelInfo()
        // Create a domain
        riffle.SetFabric("ws://192.168.1.99:8000")
        cmd := "test"
        // Create the domain objects
        app := riffle.NewDomain("xs.node")
        sender := app.Subdomain("can")

        sender.Join()
        time.Sleep(200 * time.Millisecond)
        sender.Publish("cmd", cmd)
        time.Sleep(200 * time.Millisecond)
        sender.Publish("cmd", cmd)
}
