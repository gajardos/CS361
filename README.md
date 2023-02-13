# CS361
CS 361 Software Engineering 1 project. Mortgage rate calculator desktop app.

For current interest rate microservice make requests via using ZMQ for communication.
Example program including calling and receiving using python:

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to get rate server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

credit_score = 650

#  Do a request and wait for a response
socket.send_string(f"{credit_score}")

#  Get the reply
message = socket.recv_string()

# Close and unbind socket once done
socket.unbind("tcp://*:5555")
socket.close()
context.term()
