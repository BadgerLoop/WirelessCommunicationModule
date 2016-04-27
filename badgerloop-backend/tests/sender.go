package main

import "time"
import "github.com/exis-io/core"
import "github.com/exis-io/core/goRiffle"
import "math/rand"

func main() {
	core.LogLevel = core.LogLevelDebug
	var err error
	var conn core.Connection
	core.Fabric = "ws://192.168.99.100:8000"
	// Create a domain
	if conn, err = goRiffle.Open(core.Fabric); err != nil {
		core.Error("Unable to connect")
	} else {
		app := core.NewDomain("xs.node", nil)
		backend := app.Subdomain("backend")
		datasource := app.Subdomain("datasource")

		// Join the fabric
		go datasource.Join(conn)

		// Super hack - sleep to let the connection come up
		time.Sleep(5 * time.Millisecond)
		var ep string
		var ret []interface{}
		ret = append(ret, rand.Intn(100))
		ep = "demo"
		// Do important stuff
		for {
			// Make the call to get the data we need
			//core.Info("Sending %v, %v", ep, ret)
			defer func(){main()}()
			backend.Publish(ep, ret)
			
			time.Sleep(10 * time.Millisecond)
		}
	}
}