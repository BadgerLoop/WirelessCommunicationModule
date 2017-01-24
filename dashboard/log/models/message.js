var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var MessageSchema = new Schema({
	timestamp: {type: Date, default: Date.now },
	sid: String,
	type: String,
	data: String
});

module.exports = mongoose.model('Message', MessageSchema);