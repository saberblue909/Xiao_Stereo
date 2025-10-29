const path = require("path");
const express = require("express");
const WebSocket = require("ws");
const app = express();
const fs = require("fs"); // Import the fs module

const WS_PORT  = 8888;
const HTTP_PORT = 8000;
let lastImageTime = Date.now();

const wsServer = new WebSocket.Server({port: WS_PORT}, ()=> console.log(`WS Server is listening at ${WS_PORT}`));

let connectedClients = [];
wsServer.on('connection', (ws, req) => {
    console.log('Connected');

    ws.on('message', (data) => {
        if (data.indexOf("WEB_CLIENT") !== -1) {
			connectedClients.push(ws);
			console.log("WEB_CLIENT ADDED");
			return;
		}
        const currentTime = Date.now();
         if (currentTime - lastImageTime > 1000) {
           imageCounter = 1;
         }
     
         const filename1 = `CAM1_${imageCounter}.jpeg`;
         const filename2 = `CAM2_${imageCounter}.jpeg`;
     
         fs.writeFile(path.join(__dirname, "images/cam1", filename1), data, (err) => {
           if (err) throw err;
           console.log(`${filename1} saved!`);
         });
     
         fs.writeFile(path.join(__dirname, "images/cam2", filename2), data, (err) => {
           if (err) throw err;
           console.log(`${filename2} saved!`);
         });
     
         lastImageTime = currentTime;
         imageCounter++;
     
        connectedClients.forEach((ws,i) => {
            if(connectedClients[i] == ws && ws.readyState === ws.OPEN){
                ws.send(data);
            }else{
                connectedClients.splice(i ,1);
            }
        })
    });
    ws.on("error", (error) => {
		console.error("WebSocket error observed: ", error);
	});
});

app.use(express.static("."));
app.get('/client',(req,res)=>res.sendFile(path.resolve(__dirname, './client.html')));
app.listen(HTTP_PORT, ()=> console.log(`HTTP server listening at ${HTTP_PORT}`));