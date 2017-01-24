# Badgerloop Competition Dashboard
### Dashboard Client
+ Run **npm install && bower install**
+ Serve client with **grunt serve**
+ The Dashboard client is served on **port 9000**

### Database Backend
+ Start a MongoDB **daemon instance**, or modify **server.js** to point to a hosted DB.
+ Run **node server.js** to start the express server.
+ The express server is served on **port 8000**

### Database Client
+ The database client is a separate angular app
+ The app is hosted through the express server
+ Point your browser to **localhost:8000**