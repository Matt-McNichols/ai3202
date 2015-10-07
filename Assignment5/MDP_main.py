#!/usr/bin/python
import Queue
import sys #for command line args
import math
from MDP import graph


#### CALLING CODE STARTS HERE
g=graph(8,10,sys.argv[1],float(sys.argv[2]));        #8 rows and #10 col
g.value_iteration([7,0],[0,9]);
