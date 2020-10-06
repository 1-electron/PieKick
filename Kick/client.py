import socket
import numpy as np
import jsonpickle
import os

from .utils import fetch

def from_bytes(b):
    """convert bytes back to python object.

    convert bytes -> json -> python object.
    """
    j = b.decode()  # from bytes to json
    o = jsonpickle.decode(j)  # from json to python object
    return o


def up(fname):
    """send fname to server and retrieve corresponding results.
    
    # https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python
    """
    # get endpoint information from config file
    h = fetch("hostname")
    p = int(fetch("port"))  # convert str to int
    
    # create socket and connect with server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((h, p)) 

    # read source as bytes and send bytes to server
    with open(fname, "rb") as f:
        l = f.read(1024)
    s.send(l) 
        
    # receive results from server and unpack bytes
    res = s.recv(1024)
    o = from_bytes(res)  # https://markhneedham.com/blog/2018/04/07/python-serialize-deserialize-numpy-2d-arrays/
    # o = np.frombuffer(res)
    
    # close the connection 
    if res:
        s.close()
        return o
    else:
        raise ValueError