#!/usr/bin/python

import Queue
import sys #for command line args
import math


def printV(argument, verbosity):
    master_verb=1;
    if((verbosity > master_verb) is True):
        print argument;
