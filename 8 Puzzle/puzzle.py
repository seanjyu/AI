
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import heapq as H
import resource


## Class represent a single puzzle state, used to keep track of cost and parent
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """  
        newboard=list(self.config)
        newcost=self.cost+1
        pos=newboard.index(0)
        if pos>2:
          newboard[pos],newboard[pos-3]=newboard[pos-3],newboard[pos]
          return PuzzleState(newboard,3,parent=self,action='Up',cost=newcost)

      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        newboard=list(self.config)
        newcost=int(self.cost)+1
        pos=newboard.index(0)
        if pos<6:
          newboard[pos],newboard[pos+3]=newboard[pos+3],newboard[pos]
          return PuzzleState(newboard,3,parent=self,action='Down',cost=newcost)
        
      
    def move_left(self):
        """Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        newboard=list(self.config)
        newcost=int(self.cost)+1
        pos=newboard.index(0)
        if pos!= 0 and pos!= 3 and pos!= 6:
          newboard[pos],newboard[pos-1]=newboard[pos-1],newboard[pos]
          return PuzzleState(newboard,3,parent=self,action='Left',cost=newcost)
        

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        newboard=list(self.config)
        newcost=int(self.cost)+1
        pos=newboard.index(0)
        if pos != 2 and pos!= 5 and pos!= 8:
          newboard[pos],newboard[pos+1]=newboard[pos+1],newboard[pos]
          return PuzzleState(newboard,3,parent=self,action='Right',cost=newcost)
 
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

def writeOutput(results):
    path=get_path(results[0])
    f= open("output.txt","w+")
    f.write("path_to_goal: %s\n" %(path))
    f.write("cost_of_path: %s\n" %(results[0].cost))
    f.write("nodes_expanded: %s\n" %(results[2]))
    f.write("search_depth: %s\n" %(results[0].cost))
    f.write("max_search_depth: %s\n" %(results[1]))
    f.write("running_time: %s\n" %(results[4]))
    f.write("max_ram_usage: %s\n" %(results[3]))
    f.close()
    
  
def bfs_search(initial_state):
    """BFS search"""
    #Intialize variables and start time. Use queue functions. Put initial state in queue.
    start_time=time.time()
    q=Q.Queue()
    maxdep=0
    nexp=-1 #Do not count initial state as node
    q.put(initial_state)
    frontierconfigs=set()
    explored=set()
    maxram=resource.getrusage(resource.RUSAGE_SELF)[2]*2**(-10)
    
    while q.empty() != True:
      #get node  
      node=q.get()
      #add to explored set
      explored.add(tuple(node.config))
      #increase explored counter
      nexp=nexp+1
      #check if node is goal state, if true writeoutputs.
      if test_goal(node)==node:
          total_time=time.time()-start_time
          results=[node,maxdep,nexp,maxram,total_time]
          return writeOutput(results)
        
      #expand node
      neighbors=node.expand()

      #check if expanded nodes are in frontier and explored, if not put into queue and update frontier and explored sets.    
      for neighbor in neighbors:          
        if tuple(neighbor.config) not in explored:
            if tuple(neighbor.config) not in frontierconfigs:
                q.put(neighbor)
                if neighbor.cost>maxdep:
                      maxdep=neighbor.cost
                frontierconfigs.add(tuple(neighbor.config))

                #Check maximum ram usage
                nmaxram=resource.getrusage(resource.RUSAGE_SELF)[2]*2**(-10)
                if nmaxram > maxram:
                        maxram=nmaxram
            

def dfs_search(initial_state):
    """DFS search"""
    #Intialize variables and start time, use list and pop. Append initial state to list.
    start_time=time.time()
    s=[]
    maxdep=0
    nexp=-1 #Do not count initial state as node
    s.append(initial_state)
    frontierconfigs=set()
    explored=set()
    maxram=resource.getrusage(resource.RUSAGE_SELF)[2]*2**(-10)
    while len(s) > 0:
      #get node   
      node=s.pop()
      #add to explored set
      explored.add(tuple(node.config))
      #increase explored counter
      nexp=nexp+1
      #check if node is goal state, if true writeoutputs.
      if test_goal(node)==node:
          total_time=time.time()-start_time
          results=[node,maxdep,nexp,maxram,total_time]
          return writeOutput(results)

      #expand node
      neighbors=node.expand()

      #check if expanded nodes are in frontier and explored, if not put into stack. Note for loop in reverse order since using lifo stack   
      for i in reversed(range(len(neighbors))):
        if tuple(neighbors[i].config) not in explored:
                if tuple(neighbors[i].config) not in frontierconfigs:
                    s.append(neighbors[i])
                    if neighbors[i].cost>maxdep:
                      maxdep=neighbors[i].cost
                    frontierconfigs.add(tuple(neighbors[i].config))
                    
                    #Check maximum ram usage
                    nmaxram=resource.getrusage(resource.RUSAGE_SELF)[2]*2**(-10)
                    if nmaxram > maxram:
                        maxram=nmaxram

def A_star_search(initial_state):
    """A * search"""
    #Intialize variables and start time, use heap, push initial state to heap.
    start_time=time.time()
    h=[]
    H.heapify(h)
    maxdep=0
    nexp=-1 #Do not count initial state as node
    frontierconfigs=set()
    explored=set()
    H.heappush(h,[0,0,0,initial_state])
    maxram=resource.getrusage(resource.RUSAGE_SELF)[2]*2**(-10)

    while len(h) > 0:
        #get node
        node=H.heappop(h)
        #increase explored counter
        nexp=nexp+1

        #add to explored set
        explored.add(tuple(node[3].config))
        #check if node is goal state, if true writeoutputs.
        if test_goal(node[3])==node[3]:
            total_time=time.time()-start_time
            results=[node[3],maxdep,nexp,maxram,total_time]
            return writeOutput(results)
        #expand node
        neighbors=node[3].expand()
        
        #check if expanded nodes are in frontier and explored, if not put into heap. Note no key decrease since cannot revist previous config
        for neighbor in neighbors:
            if tuple(neighbor.config) not in explored:
                if tuple(neighbor.config) not in frontierconfigs:
                    #prioritize based on cost, move and time
                    tcost=calculate_total_cost(neighbor)
                    if neighbor.action == 'Up':
                        move=1
                    elif neighbor.action == 'Down':
                        move=2
                    elif neighbor.action == 'Left':
                        move=3
                    else:
                        move=4   
                    H.heappush(h,[tcost,move,time.time(),neighbor])
                    if neighbor.cost>maxdep:
                        maxdep=neighbor.cost
                    frontierconfigs.add(tuple(neighbor.config))

                    #Check maximum ram usage
                    nmaxram=resource.getrusage(resource.RUSAGE_SELF)[2]*2**(-10)
                    if nmaxram > maxram:
                        maxram=nmaxram
                    
def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    cost=state.cost
    config=state.config
    mcost=0
    #Calculate manhattan value
    for i in range(1,8):
        idx=config.index(i)
        mcost=mcost+calculate_manhattan_dist(idx, i, 3)
    return mcost+cost

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    srow=idx // n
    scol=idx % n
    grow=value // n
    gcol= value % n
    return abs(grow-srow)+abs(gcol-scol)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    if puzzle_state.config == [0,1,2,3,4,5,6,7,8]:
      return puzzle_state
 
def get_path(Goal_state):
    """Get Path Based on Parent"""
    state=Goal_state
    path=[]
    move=None
    #append moves until intial
    while move != "Initial":
        path.append(state.action)
        state=state.parent
        move=state.action
    return path[::-1]
    
# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
                        


        
          
