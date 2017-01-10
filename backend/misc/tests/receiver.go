package main

import "fmt"
import "github.com/exis-io/core"
import "github.com/exis-io/core/riffle"


func sub(name string) {
	riffle.Info("Pub received! Name: %s", name)
}

func main() {
	core.LogLevel = core.LogLevelDebug
	// Create a domain
	riffle.SetFabric("ws://192.168.1.99:8000")

	// Create the domain objects
	app := riffle.NewDomain("xs")
	receiver := app.Subdomain("cmd")
	
	defer func(){main()}()
	receiver.Join()

	receiver.Subscribe("exis", func(a string) {
		fmt.Println("Got something ")
	})

}