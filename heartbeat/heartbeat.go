package main

import "time"
import "github.com/exis-io/core/riffle"


func main() {
        riffle.SetLogLevelInfo()
        // Create a domain
        riffle.SetFabric("ws://192.168.1.99:8000")
        // Create the domain objects
        app := riffle.NewDomain("xs.node")
        sender := app.Subdomain("hb")

        sender.Join()
        for {
                sender.Publish("hb", "hb")
                time.Sleep(1 * time.Second)
        }
}