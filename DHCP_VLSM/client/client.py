#!/usr/bin/python

import socket
import subprocess
import os
from threading import Thread
import datetime
import re
import time
import sys

host = ""
port = 60024

s = socket.socket()
s.connect((host, port))

arglen=len(sys.argv)

if arglen==1:
    #take computer mac
    f = os.popen("ifconfig -a | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'| head -1")
    for a in f:
        temp=a
    ans=temp[:-1].upper()
    print "MAC address is:      ",ans
    s.send(ans)
    myip = s.recv(1024)
    print myip


elif arglen==3:
    ans=sys.argv[2];
    r = re.compile('^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$')
    if r.match(ans) is not None:
        print "MAC address is:      ",ans
        s.send(ans)
        myip = s.recv(1024)
        print myip

    else:
        print "Error:argument is not in correct mac formate\n"

else:
    print "Error:There should be either 1 or 3 arguments\n";

#print "IP address is"+ myip +"\n"
#print arglen;
    #command = raw_input("prompt> ")
    #kaato = command.split(" ")
s.close()
#print('connection closed')
