CS_361

Work for Software Engineering I [CS361]

Spray Cave Climbing App

An app to upload and view custom rock climbs for the Dixon cave climbing wall.

Climb Data Microservice

A microservice to store and send data for custom climbs. Uses zeromq to communicate over a network.

Connect to server

import zmq

context = zmq.Context() socket = context.socket(zmq.REQ) socket.connect("tcp://localhost:5555")

Sending requests

Requests are made using json objects. The first key of this object is "method", which can be either "add" or "get.

Add method

The add method requires one more key, which is "data". The value of this key needs to be a json object containing data for a climb. The microservice will respond with a json object containing the status of the request, which will either be "success", or "fail" if the data couldn't be stored.

Example usage: socket.send_json({"method": "add", "data": climb}) response = socket.recv_json()

where climb is an object containing json data

Get method

The get method requests all of the data stored by the microservice. The microservice will respond with the json object containing this data (stored objects in an array called "climbData")

Example usage: socket.send_json({"method": "get"}) response = socket.recv_json()
