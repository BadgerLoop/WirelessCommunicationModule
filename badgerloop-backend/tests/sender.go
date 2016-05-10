package main

import "time"
//import "github.com/exis-io/core"
import "github.com/exis-io/core/riffle"
import "math/rand"

func main() {
	//core.LogLevel = core.LogLevelDebug
	// Create a domain
	riffle.SetFabric("ws://192.168.99.100:8000")

	// Create the domain objects
	app := riffle.NewDomain("xs.node")
	sender := app.Subdomain("sender")

	sender.Join()
	
		// Super hack - sleep to let the connection come up
		var ep string
		ep = "demo"
		time.Sleep(200 * time.Millisecond)
		for {
			// Make the call to get the data we need
			//core.Info("Sending %v, %v", ep, ret)
			time.Sleep(100 * time.Millisecond)
			defer func(){main()}()
			sender.Publish(ep, rand.Intn(100))
			
	}
	sender.Listen()
}