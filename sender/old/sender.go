package main

import "strconv"
import "os/exec"
import "time"
import "github.com/exis-io/core"
import "github.com/exis-io/core/goRiffle"
import "strings"

func parse(str string) (string, []interface{}, error) {
	var err error
	var ret []interface{}
	var ep string

	str = strings.Trim(str, "\n")
	sp := strings.Split(str, "_")
	core.Info("%v", sp)
	ep = sp[0] + "_" + sp[1]

	switch ep {
	case "vcm_gyro":
		core.Info("Got gyro")
	default:
		core.Error("DEFAULT")
	}

	for i := 2; i < len(sp); i++ {
		s := sp[i]
		if f, er := strconv.ParseFloat(s, 64); er == nil {
			ret = append(ret, f)
		} else {
			return ep, ret, er
		}
	}
	return ep, ret, err
}

func main() {
	core.LogLevel = core.LogLevelDebug
	var err error
	var conn core.Connection
	core.Fabric = "ws://192.168.1.4:8000/ws"
	// Create a domain
	if conn, err = goRiffle.Open(core.Fabric); err != nil {
		core.Error("Unable to connect")
	} else {
		app := core.NewDomain("xs.demo.badgerloop.bldashboard", nil)
		backend := app.Subdomain("backend")
		datasource := app.Subdomain("datasource")

		// Join the fabric
		go datasource.Join(conn)

		// Super hack - sleep to let the connection come up
		time.Sleep(1 * time.Second)

		// Do important stuff
		for {
			// Make the call to get the data we need
			if out, err := exec.Command("./can/can_parse_single").Output(); err != nil {
				core.Error("Error %v", err)
			} else {
				str := string(out)
				if ep, pyld, err := parse(str); err == nil {
					core.Info("Sending %v, %v", ep, pyld)
					backend.Publish(ep, pyld)
				}
			}
			time.Sleep(1 * time.Second)
		}
	}
}
