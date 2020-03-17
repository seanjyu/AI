from copy import deepcopy
import time
import sys
"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def check(board,val,row,col):
    #check col
    checkpos=row+str(col)
    for i in ROW:
        
        pos=i+str(col)
        if board[pos]==val and pos!=checkpos:
            return False
        
    #check row
    for k in COL:
        pos=row+str(k)
        if board[pos]==val and pos!=checkpos:
            return False

    #check box
    if row in ROW[0:3]:
        if str(col) in COL[0:3]:
            for l in ROW[0:3]:
                for m in COL[0:3]: 
                    if board[l+m]==val and l+m!=checkpos:
                        return False                    
        if str(col) in COL[3:6]:
            for l in ROW[0:3]:
                    for m in COL[3:6]: 
                        if board[l+m]==val and l+m!=checkpos:
                            return False
        if str(col) in COL[6:9]:
            for l in ROW[0:3]:
                    for m in COL[6:9]:
                        if board[l+m]==val and l+m!=checkpos:
                            return False
    if row in ROW[3:6]:
        if str(col) in COL[0:3]:
            for l in ROW[3:6]:
                for m in COL[0:3]:
                    if board[l+m]==val and l+m!=checkpos:
                        return False
                    
        if str(col) in COL[3:6]:
            for l in ROW[3:6]:
                    for m in COL[3:6]: 
                        if board[l+m]==val and l+m!=checkpos:
                            return False
        if str(col) in COL[6:9]:
            for l in ROW[3:6]:
                    for m in COL[6:9]: 
                        if board[l+m]==val and l+m!=checkpos:
                            return False
            
    if row in ROW[6:9]:
        if str(col) in COL[0:3]:
            for l in ROW[6:9]:
                for m in COL[0:3]:
                    if board[l+m]==val and l+m!=checkpos:
                        return False
                    
        if str(col) in COL[3:6]:
            for l in ROW[6:9]:
                    for m in COL[3:6]:
                        if board[l+m]==val and l+m!=checkpos:
                            return False
        if str(col) in COL[6:9]:
            for l in ROW[6:9]:
                    for m in COL[6:9]:
                        if board[l+m]==val and l+m!=checkpos:
                            return False

    return True

def mrv(domain_dict, board):
    unassigned_tile = [tile for tile in domain_dict.keys() if board[tile] == 0]
    return min(unassigned_tile, key=lambda tile: len(domain_dict[tile]))

def backtracking(board):
    d=domains(board)
    finished_board = bt({},board,d)
    return finished_board
    

def bt(assignment, board,domains):
    """Takes a board and returns solved board."""
    cur_domain=deepcopy(domains)    
    


    x = [tile for tile in domains.keys() if board[tile] == 0]
    if not x:
        return board

    pos=mrv(domains, board)
    vals=cur_domain[pos]
    
    for k in vals:
        if forwardcheck(board,k,pos)==True:
            d_copy=deepcopy(domains)

            board[pos]=k

            assignment_copy = deepcopy(assignment)
            assignment_copy[pos] = k
            d=updatedomains(cur_domain,board)

            result=bt(assignment_copy,board, d)
            if result!=False:
                return result
            
            board[pos]=0
        d =deepcopy(domains)
    return False

def forwardcheck(board, pos, k):
    board[pos]=k
    allvars=[]
    for i in ROW:
        for j in COL:
            if board[i+j]==0:
                posvar=[]
                for k in range(1,10):
                    if check(board,k,i,j):
                        posvar.append(k)
                allvars.append(posvar)
    if any (x==[] for x in allvars):
        return False
    else:
        return True

def checkdone(board):
    for i in ROW:
        for j in COL:
            if check(board,board[i+j],i,j)==False:
               return False 
    return True

def domains(board):
    allvars=[]
    allboardpos=[]
    varsdict={}
    for i in ROW:
        for j in COL:
            if board[i+j]==0:
                posvar=[]
                boardpos=str(i+j)
                allboardpos.append(boardpos)
                for k in range(1,10):
                    if check(board,k,i,j):
                        posvar.append(k)
                allvars.append(posvar)
                varsdict[str(i+j)]=posvar
    if len(allvars)>0:
        minvars=min(allvars)
        ind=allvars.index(minvars)
        orddict={a: b for a, b in sorted(varsdict.items(), key=lambda item: len(item[1]))}
        return orddict
        
    return False

def updatedomains(domain,board):
    allvars=[]
    allboardpos=[]
    varsdict={}
    for i in domain:
        posvar=[]
        boardpos=i
        allboardpos.append(boardpos)
        for k in range(1,10):
            if check(board,k,i[0],i[1]):
                posvar.append(k)
        allvars.append(posvar)
        varsdict[i]=posvar
    if len(allvars)>0:
        minvars=min(allvars)
        ind=allvars.index(minvars)
        orddict={a: b for a, b in sorted(varsdict.items(), key=lambda item: len(item[1]))}
        return orddict
        
    return False

                        
                        
    
if __name__ == '__main__':
    #  Read boards from source.
    #start_time=time.time()
    #src_filename = 'sudokus_start.txt'
    #try:
    #    srcfile = open(src_filename, "r")
    #    sudoku_list = srcfile.read()
    #except:
    #    print("Error reading the sudoku file %s" % src_filename)
    #    exit()

    # Setup output file
    #out_filename = 'output.txt'
    #outfile = open(out_filename, "w")

    # Solve each board using backtracking
    #for line in sudoku_list.split("\n"):

    #    if len(line) < 9:
    #        continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
    #    board = { ROW[r] + COL[c]: int(line[9*r+c])
    #              for r in range(9) for c in range(9)}

        # Print starting board. TODO: Comment this out when timing runs.
        #print_board(board)

        # Solve with backtracking
     #   solved_board = backtracking(board)

        # Print solved board. TODO: Comment this out when timing runs.
        #print_board(solved_board)
        # Write board to file
     #   outfile.write(board_to_string(solved_board))
     #   outfile.write('\n')

    #outfile.close()
    #endtime=time.time()-start_time
    #print(endtime)
    #print("Finishing all boards in file.")
    line=sys.argv[1]
    board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}
    solved_board = backtracking(board)
    f = open('output.txt', "w")
    f.write(board_to_string(solved_board))
    f.close()
