package main

import "time"
import "github.com/exis-io/core/riffle"


func main() {
        riffle.SetLogLevelInfo()
        // Create a domain
        riffle.SetFabric("ws://badgerloop-nuc-1:8000")
        cmd := "run"
        // Create the domain objects
        app := riffle.NewDomain("xs")
        sender := app.Subdomain("node")

        sender.Join()
        time.Sleep(200 * time.Millisecond)
        sender.Publish("cmd", cmd)
        time.Sleep(200 * time.Millisecond)
        sender.Publish("cmd", cmd)
}
