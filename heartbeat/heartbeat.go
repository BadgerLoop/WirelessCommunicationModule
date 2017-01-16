package main
import "fmt"
import "time"
import "github.com/exis-io/core/riffle"

func start_hb(ms){
        for {
                sender.Publish("hb", "hb") //May want to send heartbeat can message here
                time.Sleep(ms * time.Millisecond)
        }
}

func hb_ctrl(data){
        Heartbeat := make(chan int)
        quit := make(chan int)
        if data[0] == "run" {
                //This might need work.
                go start_hb(data[1]) {
                    select {
                    case <- Heartbeat:
                            fmt.Println("Heartbeat Stopped")
                    }
                }()
        } else if a == "stop" {
                close(quit)
}


func main() {
        riffle.SetLogLevelInfo()
        // Create a domain
        riffle.SetFabric("ws://192.168.1.99:8000")
        // Create the domain objects
        core := riffle.NewDomain("xs")
        app := core.Subdomain("node")
        app.Join()

        if e := app.Subscribe("hb_ctrl", hb_ctrl); e != nil {
                riffle.Info("Unable to subscribe to hb_ctrl endpoint", e.Error())
        } else {
                riffle.Info("Subscribed to hb_ctrl endpoint!")
        }
        app.Listen()
        

}