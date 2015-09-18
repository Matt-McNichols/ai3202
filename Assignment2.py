#!/usr/bin/python
import Queue
import sys #for command line args
import math

#factor in mountains
#print outputs nicer
#make world a command line arg

class node(object):
  def __init__(self,key=None):
    self.key=key;
    self.location=[sys.maxint,sys.maxint];
    self.parent=[sys.maxint,sys.maxint];
    self.F=sys.maxint;
    self.G=None;
    self.H=None;



class graph(object):

  def __init__(self,master_row=None,master_col=None,world=None):

    if world is None:
      print "matt you suck no world";
      return

    with open(world) as f:
      self.world_master = [[node(int(x)) for x in line.split()] for line in f]

    self.openList=[];
    self.closedList=[];
    self.master_row=master_row;
    self.master_col=master_col;
    # At this point world matrix is set up an open/closed lists
    # are initialized





  def printInfo(self):
    print "master_row: ",self.master_row,"\n","master_col: ",self.master_col;
    print "-----------------h_scores-----------"
    for i in range(self.master_row):
      print [index.H for index in self.world_master[i][:]];
    print "-----------------g_scores-----------"
    for i in range(self.master_row):
      print [index.G for index in self.world_master[i][:]];
    print "-----------------node_locations_scores-----------"
    for i in range(self.master_row):
      print [index.location for index in self.world_master[i][:]];



  def set_H_manhattan(self,end=[None,None]):
    if end is not [None,None]:
    #calculate f score = g_score + h_score
      for r in range(self.master_row):
        for c in range(self.master_col):
          row_delta=abs(end[0]-r);
          col_delta=abs(end[1]-c);
          self.world_master[r][c].H= int(row_delta+col_delta);
          # Also set location while your at it
          self.world_master[r][c].location=[int(r),int(c)];

  def set_H_crow(self,end=[None,None]):
    if end is not [None,None]:
    #calculate f score = g_score + h_score
      for r in range(self.master_row):
        for c in range(self.master_col):
          row_delta=abs(end[0]-r);
          col_delta=abs(end[1]-c);
          H=math.sqrt((row_delta*row_delta)+(col_delta*col_delta));
          self.world_master[r][c].H= H;
          # Also set location while your at it
          self.world_master[r][c].location=[int(r),int(c)];


  def closedList_walls(self):
    for r in range(self.master_row):
      for node in self.world_master[r][:]:
        if node.key is 2:
          node.parent=[-1,-1];
          self.closedList.append(node);



  def set_F(self,c_node,n_node):
    new_g=int(c_node.G+n_node[1]);
    new_f=new_g+n_node[0].H;
#print new_g;
    if n_node[0] not in self.openList:
      n_node[0].G=new_g;
      n_node[0].F=new_f;
      n_node[0].parent=c_node.location;
      self.openList.append(n_node[0])
    elif (n_node[0].G > new_g) is True:
       n_node[0].F=new_f
       n_node[0].G=new_g
       n_node[0].parent=c_node.location


  def openList_update(self):
    # sort f from largest to smallest
    from operator import attrgetter;
    self.openList.sort(key=attrgetter('F'),reverse=True);



  def neighbor(self,r=None,c=None):
    if r is None or c is None:
      print "neighbor was called incorrectly";
      return None;
    else:
      n=[]
      Dir_10=[[r-1,c],[r,c-1],[r+1,c],[r,c+1]];
      Dir_14=[[r-1,c-1],[r+1,c+1],[r+1,c-1],[r-1,c+1]];
      for location in Dir_10:
        if (location[0] < self.master_row) is True and (location[1] < self.master_col)is True and (location[0]>=0)is True and (location[1]>=0) is True and self.world_master[location[0]][location[1]] not in self.closedList:
          temp=[self.world_master[location[0]][location[1]],10];
          if temp[0].key is 1:
            temp[1]+=10;
          n.append(temp);

      for location in Dir_14:
        if (location[0] < self.master_row)is True and (location[1] < self.master_col)is True and (location[0]>=0)is True and (location[1]>=0) is True and self.world_master[location[0]][location[1]] not in self.closedList:
          temp=[self.world_master[location[0]][location[1]],14];
          if temp[0].key is 1:
            temp[1]+=10;
          n.append(temp);

      return n;





  def build_path(self,end_location):
    self.path_cost=self.world_master[end_location[0]][end_location[1]].G
    self.path_nodes=Queue.LifoQueue();
    current_node=self.world_master[end_location[0]][end_location[1]];
    self.path_nodes.put(current_node);
    while (current_node.parent!=self.start)is True:
      current_node=self.world_master[current_node.parent[0]][current_node.parent[1]];
      self.path_nodes.put(current_node);
    self.path_node=self.world_master[current_node.location[0]][current_node.location[1]];

    print "path locations: ";
    count=0;
    print self.start
    while not self.path_nodes.empty():
      p=self.path_nodes.get()
      print  p.location;
      count=count+1;

    print "number of locations in path: ", count;
    print "total cost of path:", self.path_cost;




















  def a_star(self,start_location=[None,None],end_location=[None,None]):
    #check valid start and end

    #set start and end
    self.start=start_location;
    self.end=end_location;

    # Each nodes H score will be static calculate here
    self.set_H_crow(self.end);
    # put all wall nodes in the closed list
    self.closedList_walls();
    # set start node g to zero
    self.world_master[self.start[0]][self.start[1]].G=0;
    self.world_master[self.start[0]][self.start[1]].parent=[-11,-11];
    #push the start node into openList
    self.openList.append(self.world_master[self.start[0]][self.start[1]]);



    #enter the loop until the end node is in closedList
    while len(self.openList) != 0:
      self.c_node=self.openList.pop()
      self.closedList.append(self.c_node)

      # check if end node is c_node
      if self.c_node is self.world_master[end_location[0]][end_location[1]]:
        print "path is complete";
        self.build_path(end_location);
        break;

      # Call neighbor function that returns a list of touples [nonde, weight]
      self.c_neighbor=self.neighbor(self.c_node.location[0],self.c_node.location[1]);

      for n_node in self.c_neighbor:
        self.set_F(self.c_node,n_node)
      self.openList_update()







#### CALLING CODE STARTS HERE
g=graph(8,10,sys.argv[1]);        #8 rows and #10 col
g.a_star([7,0],[0,9]);             # start: row=2, col=3
