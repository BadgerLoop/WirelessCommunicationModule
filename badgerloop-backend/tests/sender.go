package main

import "time"
import "github.com/exis-io/core"
import "github.com/exis-io/core/riffle"
import "math/rand"

func main() {
	core.LogLevel = core.LogLevelDebug
	// Create a domain
	riffle.SetFabric("ws://192.168.99.100:8000")

	// Create the domain objects
	app := riffle.NewDomain("xs.node")
	sender := app.Subdomain("sender")

	sender.Join()
	
		// Super hack - sleep to let the connection come up
		time.Sleep(5 * time.Millisecond)
		var ep string
		ep = "demo"
		// Do important stuff
		for {
			// Make the call to get the data we need
			//core.Info("Sending %v, %v", ep, ret)
			defer func(){main()}()
			sender.Publish(ep, rand.Intn(100))
			time.Sleep(10 * time.Millisecond)
	}
	sender.Listen()
}