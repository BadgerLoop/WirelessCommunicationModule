package main

import (
"time"
riffle "github.com/exis-io/core/riffle"

)

func sub(name string) {
	riffle.Info("Pub received! Name: %s", name)
}

func main() {
        riffle.SetLogLevelInfo()
        // Create a domain
        riffle.SetFabric("ws://192.168.1.99:9000")

        // Create the domain objects
        app := riffle.NewDomain("xs.node")
        receiver := app.Subdomain("sender")

        receiver.Join()
        time.Sleep(200 * time.Millisecond)
        if e := receiver.Subscribe("demo", sub); e != nil {
             riffle.Info("Unable to subscribe: ", e.Error())
        } else {
             riffle.Info("Subscribed!")
        }
        receiver.Listen()
}
