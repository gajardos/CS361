# Author: Sebastian Gajardo
# Date: 2/15/2023
# Course: CS 361 Software Engineering 1
# Description: Client used to get current mortgage rates from FRED API with a credit score adjustment from partners microservice.

import zmq

def get_rate(credit_score: int):
    """ Gets average mortgage rate adjusted for credit score from partners microservice.

    Args:
        credit_score (int): Credit score that user inputs into desktop app.
    """
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to get rate server")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    #  Send request, waiting each time for a response
    print(f"Sending request {credit_score} …")
    socket.send_string(f"{credit_score}")

    #  Get the reply
    message = socket.recv_string()
    print(f"Received reply [ {message} ]")

    # Close and unbind socket once done
    socket.unbind("tcp://localhost:5555")
    socket.close()
    context.term()
    
    return float(message)