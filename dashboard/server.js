var path = require('path');
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
var Message = require('./log/models/message.js');

var express = require('express');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);
var riffle = require('jsriffle');

riffle.setFabric("ws://localhost:8000");
var exis_node = riffle.Domain("xs.node");



riffle.setLogLevelDebug();
var core = riffle.Domain("xs");
var node = core.subdomain("node");
// Create event handler

app.set('port', process.env.PORT || 6000);
app.use(express.static(path.join(__dirname,  '/log/client')));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Competition Connection

mongoose.connect('mongodb://localhost:27017/badgerloop', function(error) {
	if(error) console.log(error);
	else console.log('Connected to competition database');
});

node.onJoin = function() {

    // Example Pub/Sub Basic - a very basic pub/sub example

    this.subscribe("can", riffle.want(function(data) {
    	console.log("RECEIVED MESSAGE FROM CAN ENDPOINT");
        console.log(data); 
        for (var i=0; i<data.length; i++){
 //Data will be in the format [timestamp, sid, message type, data]
	var msg = new Message({
	    timestamp: new Date(parseFloat(data[i][0])), 
	    sid: data[i][1], 
	    type: data[i][2],
	    data: data[i][3]
	});

	msg.save(function(err, msg) {
	  if (err) return console.error(err);
	  console.dir(msg);
	}); 
	}
	},[[String]]));

};
node.join()


// exis_node.subscribe("can", function(data) {
// 	console.log("received message")
// 	console.log(data)
// //Data will be in the format [timestamp, sid, message type, data]
// 	var msg = new Message({
// 	    timestamp: new Date(data[0]), 
// 	    sid: data[1], 
// 	    type: data[2],  // Notice the use of a String rather than a Number - Mongoose will automatically convert this for us.
// 	    data: data[3]
// 	});

// 	msg.save(function(err, msg) {
// 	  if (err) return console.error(err);
// 	  console.dir(msg);
// 	}); 
// });
// /new Date().getTime()
//node.publish('can',["","00","00","00 00"])
// Hosted Connection

// var MONGOLAB_URI = 'mongodb://heroku_wrpm8z2c:adbk172h0lfvugpggqt4hdr2d9@ds153815.mlab.com:53815/heroku_wrpm8z2c';

// mongoose.connect(MONGOLAB_URI, function(error) {
// 	if(error) console.log(error);
// 	else console.log('Connected to hosted database');
// });

// Router Setup
var router = express.Router();

// Notify on any request
router.use(function(req, res, next) {
	console.log('Request Made');
	next();
});

router.get('/', function(req, res) {
	res.json({ message: 'Message Logging API' });
});

// Route for CAN messages
router.route('/messages')
	.post(function(req, res) {

		var message = new Message();
		message.timestamp = req.body.timestamp;
		message.sid = req.body.sid;
		message.type = req.body.type;
		message.data = req.body.data;


		message.save(function(err) {
			if(err) res.send(err);
			else {
				res.json({ message: 'Message created' });
				io.sockets.emit('new-entry', {});

			}
		});

		

	})

	.get(function(req, res) {
		Message.find(function(err, messages) {
			if(err) res.send(err);
			else { res.json(messages); }
		});
	});

// Register base route
app.use('/logger', router);

server.listen(app.get('port'), function() {
	console.log('Collection Server running on port: 6000');
});
