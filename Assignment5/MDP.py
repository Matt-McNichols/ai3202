#!/usr/bin/python
import Queue
import sys #for command line args
import math



#   FIXME: matt
#   a MDP is a non-deterministic, sequential search problem with a Markovian transition
#   model and additive rewards.

#   FIXME: matt
#   Transition Function:  probablility the next state will be s' is the intended state for the given
#                      action and current state. There is a prob. of success associated with the action

#   FIXME: matt
#   Reward function: R(s, a, s'). The reward for taking action a to move from state s to state s'.

#   FIXME: matt
#   utility function:  The quality measure of a reward sequence u(Ra,LRb,L^2Rc...)




#   FIXME: matt
#   Types of utility functions:
#   1. Bellman equation
#   2. value iteration (used for this assignment)



####################################################################################################
class node(object):
  def __init__(self,key=None):
    self.key=key;
    self.R=None;
    self.location=[sys.maxint,sys.maxint];
    self.parent=[None,None];
    self.north=0;
    self.east=0;
    self.south=0;
    self.west=0;
    self.P=sys.maxint;
    self.V=0;
####################################################################################################


class graph(object):

  def __init__(self,master_row=None,master_col=None,world=None,e=None):

    if world is None:
      print "matt you suck no world";
      return

    with open(world) as f:
      self.world_master = [[node(int(x)) for x in line.split()] for line in f]

    self.master_row=master_row;
    self.master_col=master_col;
    self.master_y=0.9;
    self.master_e=e;
    self.master_delta=0;
    self.setInit();
    self.setLocation();
    # At this point world matrix is set up an open/closed lists
    # are initialized
####################################################################################################

#   FIXME: matt
#   0--clear
#   1--mountain
#   2--wall
#   3--snake
#   4--farm

  def setInit(self):
    for r in range(self.master_row):
      for item in self.world_master[r][:]:
        item.V=0;
        if item.key is 0:
          item.R=0;
        elif item.key is 1:
          item.R=-1;
        elif item.key is 2:
          item.R=0;
        elif item.key is 3:
          item.R=-2;
        elif item.key is 4:
          item.R=1;
        elif item.key is 50:
          item.R=int(item.key);
          item.V=item.R;
####################################################################################################


  def setLocation(self):
    #calculate f score = g_score + h_score
      for r in range(self.master_row):
        for c in range(self.master_col):
          # Also set location while your at it
          self.world_master[r][c].location=[int(r),int(c)];
####################################################################################################



  def printInfo(self):
    print "master_row: ",self.master_row,"\n","master_col: ",self.master_col;
    print "-----------------node_locations-----------"
    for i in range(self.master_row):
      print [index.location for index in self.world_master[i][:]];
    print "-----------------node_key-----------"
    for i in range(self.master_row):
      print [index.key for index in self.world_master[i][:]];
    print "-----------------node_R-----------"
    for i in range(self.master_row):
      print [index.R for index in self.world_master[i][:]];
    print "-----------------node_V-----------"
    for i in range(self.master_row):
      print [index.V for index in self.world_master[i][:]];
    print "-----------------node_parent-----------"
    for i in range(self.master_row):
      print [index.parent for index in self.world_master[i][:]];
####################################################################################################

  def neighbor(self,r=None,c=None):
    if r is None or c is None:
      print "neighbor was called incorrectly";
      return None;
    else:
      n=[]

    #   FIXME: matt
    #
    #   make a touple with the neighbor and the cost to travel from
    #   current position

      Dir_10=[[r-1,c],[r,c-1],[r+1,c],[r,c+1]];
      for location in Dir_10:
        if (    (location[0] < self.master_row) is True and
                (location[1] < self.master_col)is True and
                (location[0]>=0)is True and
                (location[1]>=0) is True):
          n.append(self.world_master[location[0]][location[1]]);
    return n;

####################################################################################################

  def setActions(self,actions,node_s):
    if node_s.V is None:
      return node_s;
    for c_action in actions:
      #find actions relation to node_s
      if(     c_action.location[0] is node_s.location[0] and
              c_action.location[1] is (node_s.location[1]+1)):
        # c_action is east of node_s
        node_s.east=c_action;
      elif(   c_action.location[0] is node_s.location[0] and
              c_action.location[1] is (node_s.location[1]-1)):
        # c_action is west of node_s
        node_s.west=c_action;
      elif(   c_action.location[0] is (node_s.location[0]+1) and
              c_action.location[1] is node_s.location[1]):
        # c_action is south of node_s
        node_s.south=c_action;
      elif(   c_action.location[0] is (node_s.location[0]-1) and
              c_action.location[1] is node_s.location[1]):
        # c_action is north of node_s
        node_s.north=c_action;
    return node_s;
####################################################################################################



  def maxTransfer(self):
    self.p_list=[];
    self.p_north=None;
    self.p_west=None;
    self.p_south=None;
    self.p_east=None;
    # if north is a valid option
    if (self.c_node.north != 0) is True:
      if (self.c_node.north.V is not None):
        # calculate the p(node_north | c_node, north)
        self.p_north=(0.8*self.c_node.north.V);
        if (self.c_node.east != 0) is True:
          if (self.c_node.east.V is not None):
            self.p_north=self.p_north+(0.1*self.c_node.east.V);
        if (self.c_node.west != 0) is True:
          if (self.c_node.west.V is not None):
            self.p_north=self.p_north+(0.1*self.c_node.west.V);
        self.p_list.append(self.p_north);

    # if south is a valid option
    if (self.c_node.south != 0) is True:
      if (self.c_node.south.V is not None):
        # calculate the p(node_south | c_node, south)
        self.p_south=(0.8*self.c_node.south.V);
        if (self.c_node.east != 0):
          if (self.c_node.east.V is not None):
            self.p_south=self.p_south+(0.1*self.c_node.east.V);
        if (self.c_node.west != 0) is True:
          if (self.c_node.west.V is not None):
            self.p_south=self.p_south+(0.1*self.c_node.west.V);
        self.p_list.append(self.p_south);

    # if east is a valid option
    if (self.c_node.east != 0) is True:
      if (self.c_node.east.V is not None):
        # calculate the p(node_east | c_node, east)
        self.p_east=(0.8*self.c_node.east.V);
        if (self.c_node.north != 0) is True:
          if (self.c_node.north.V is not None):
            self.p_east=self.p_east+(0.1*self.c_node.north.V);
        if (self.c_node.south != 0) is True:
          if (self.c_node.south.V is not None):
            self.p_east=self.p_east+(0.1*self.c_node.south.V);
        self.p_list.append(self.p_east);

    # if west is a valid option
    if (self.c_node.west != 0) is True:
      if (self.c_node.west.V is not None):
        # calculate the p(node_east | c_node, east)
        self.p_west=(0.8*self.c_node.west.V);
        if (self.c_node.north != 0) is True:
          if (self.c_node.north.V is not None):
            self.p_west=self.p_west+(0.1*self.c_node.north.V);
        if (self.c_node.south != 0) is True:
          if (self.c_node.south.V is not None):
            self.p_west=self.p_west+(0.1*self.c_node.south.V);
        self.p_list.append(self.p_west);

    # find max action
    maxA=max(self.p_list);
    maxV=(self.master_y*maxA)+self.c_node.R;
    # calculate delta
    if((abs(self.c_node.V-maxV) > self.master_delta) is True):
      self.master_delta=abs(self.c_node.V-maxV);

    self.c_node.V=maxV;
    if (self.c_node.location == self.master_end)is True:
      self.c_node.parent=self.c_node.location;
    elif (maxA == self.p_north) is True:
      self.c_node.parent=self.c_node.north.location;
    elif (maxA == self.p_south) is True:
      self.c_node.parent=self.c_node.south.location;
    elif (maxA == self.p_east) is True:
      self.c_node.parent=self.c_node.east.location;
    elif (maxA == self.p_west) is True:
      self.c_node.parent=self.c_node.west.location;
#   FIXME: matt
#    print "max action A: ",maxA;
#    print "max value V: ",maxV;
#    print "delta: ",self.c_node.delta;
#    print "parent of c_node: ",self.c_node.parent;


####################################################################################################

  def bellman(self,node_s=None):
    # make an array of P(s'|s,a)*V(s')
    #
    if node_s is None:
      print "matt you done fucked up";
      return;
    self.actions=self.neighbor(node_s.location[0],node_s.location[1]);
    # self.c_node is the current node after north, east, south, west are set
    self.c_node=self.setActions(self.actions,node_s);
    self.maxT=self.maxTransfer();

####################################################################################################

  def value_iteration(self,start=[None,None],end=[None,None]):
    if start is [None,None] or end is [None,None]:
      return;
    else:
      self.master_start=start;
      self.master_end=end;
    # call bellman for all nodes
    # calculate a new V
    # set the delta value abs(v-v')
    # iterate until deltas are small
    self.master_check=self.master_e*((1-self.master_y)/self.master_y);
    count=0;
    while(1):
      self.master_delta=0;
      for r in range(self.master_row):
        for c in range(self.master_col):
          if(   self.world_master[r][c].key is not 2 and
                (self.world_master[r][c].location != self.master_end)is True):
            self.bellman(self.world_master[r][c]);
      count=count+1;
#print self.master_delta;
#self.printInfo();
      if ((self.master_delta < self.master_check) is True):
        break;
#      else:
#print "count",count;
#        print "delta: ",self.master_delta;
#   FIXME: matt
#      for i in range(self.master_row):
#        for index in self.world_master[i][:]:
#          if (index.delta > 5)is True:
#            self.master_done=0;
    self.reconstruct();
####################################################################################################


  def reconstruct(self):
    print "path from start to end"

    r=self.master_start[0];
    c=self.master_start[1];
    while(([r,c] != self.master_end) is True):
      print "location: ",self.world_master[r][c].location,"utility score: ",self.world_master[r][c].V;
      old_r=r;
      r=self.world_master[r][c].parent[0];
      c=self.world_master[old_r][c].parent[1];


    r=self.world_master[r][c].location[0];
    c=self.world_master[r][c].location[1];
    print "location: ",self.world_master[r][c].location,"utility score: ",self.world_master[r][c].V;
