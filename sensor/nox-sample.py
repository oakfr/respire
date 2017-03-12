#!/usr/bin/python
import serial
from collections import deque
from utils import find_device
import sys

s = serial.Serial("/dev/nox", 9600)

Q_SIZE = 10

no2_q = deque() 
o3_q = deque()

out_f = open('./output.txt', 'a')

while True:
    print ("trying to read line...")
    line = s.readline()
    print ("done")
    elements = [float(el.strip()) for el in line.split(',')]

    no2_q.append(elements[-2])
    o3_q.append(elements[-1])
    if len(no2_q) > Q_SIZE:
        no2_q.popleft()
    if len(o3_q) > Q_SIZE:
        o3_q.popleft()
    print sum(no2_q)/len(no2_q), sum(o3_q)/len(o3_q)
    out_f.write("{}, {}\n".format(sum(no2_q)/len(no2_q), sum(o3_q)/len(o3_q)))
    out_f.flush()



