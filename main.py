"""
cd /Users/computer/Root/WorkSpace/sudoku_solver
"""
import math
import time
"""
TODO:
 - Print Board at each step

"""
# # import DoublyLinkedList as DLL
class Node:
    def __init__(self, pos):
        self.pos = pos # integer pos
        self.ulink = None # pointer
        self.dlink = None # pointer
        self.len = None
        self.top = None # integer pos
        self.loc = None # tuple location
        self.row = None # item array row position 

class Header:
    def __init__(self, pos):
        self.name = None
        self.llink= None
        self.rlink= None

global l
l = 0

test_board = [[0,0,9,0,8,0,0,0,0],
            [0,6,0,0,0,0,0,7,1],
            [0,1,2,0,0,0,4,5,0],
            [0,0,8,4,0,3,1,0,0],
            [1,0,0,0,6,0,0,3,0],
            [0,0,0,0,0,8,5,0,0],
            [0,0,5,9,0,0,2,8,0],
            [0,0,0,0,4,0,0,0,7],
            [0,0,0,0,0,0,0,0,0]]


test_array = [[0, 0, 1, 0, 1, 0, 0]
            , [1, 0, 0, 1, 0, 0, 1]
            , [0, 1, 1, 0, 0, 1, 0]
            , [1, 0, 0, 1, 0, 1, 0]
            , [0, 1, 0, 0, 0, 0, 1]
            , [0, 0, 0, 1, 1, 0, 1]]

test_array2 = [[1, 0, 0, 1, 0, 0, 1]
             , [0, 1, 1, 0, 0, 1, 0]
             , [1, 0, 0, 1, 0, 1, 0]
             , [0, 1, 0, 0, 0, 0, 1]
             , [0, 0, 0, 1, 1, 0, 1]]




def transform4x4(board):
    array = []
    for j in range(4):
        for i in range(4):
            x = 2*(i//2) + (j//2)  # place cell in box
            # breakpoint()
            if board[j][i] == 0:
                for k in range(4):
                    row_insert = [0 for x in range(4*4*4)]
                    # print(row_insert, empty_row)
                    row_insert[i + 4*j] = 1  # position
                    row_insert[16 + k + 4*i] = 1 # row dependency
                    row_insert[32 + k + 4*j] = 1 # column dependency
                    row_insert[48 + k + 4*x] = 1 # box dependency
                    array.append(row_insert)
                    # print(row_insert)
                    # print(row_insert[:16], "\n", row_insert[16:32], "\n",row_insert[32:48], "\n",row_insert[48:], "\n")

            else:
                k = board[j][i]-1
                row_insert = [0 for x in range(4*4*4)]
                # print(row_insert, empty_row)
                row_insert[i + 4*j] = 1  # position
                row_insert[16 + k + 4*i] = 1 # row dependency
                row_insert[32 + k + 4*j] = 1 # column dependency
                row_insert[48 + k + 4*x] = 1 # box dependency
                array.append(row_insert)
                # print(row_insert)
                # print(row_insert[:16], "\n", row_insert[16:32], "\n",row_insert[32:48], "\n",row_insert[48:], "\n")
    return array




def transform_board(board):
    array = []
    for j in range(9):
        for i in range(9):
            x = 3*(i//3) + (j//3)  # place cell in box
            # breakpoint()
            if board[j][i] == 0:
                for k in range(9):
                    row_insert = [0 for x in range(4*9*9)]
                    # print(row_insert, empty_row)
                    row_insert[i + 9*j] = 1  # position
                    row_insert[ 81 + k + 9*i] = 1 # row dependency
                    row_insert[162 + k + 9*j] = 1 # column dependency
                    row_insert[243 + k + 9*x] = 1 # box dependency
                    array.append(row_insert)
                    # print(row_insert)

            else:
                k = board[j][i]-1
                row_insert = [0 for x in range(4*9*9)]
                # print(row_insert, empty_row)
                row_insert[i + 9*j] = 1  # position
                row_insert[ 81 + k + 9*i] = 1 # row dependency
                row_insert[162 + k + 9*j] = 1 # column dependency
                row_insert[243 + k + 9*x] = 1 # box dependency
                array.append(row_insert)
                # print(row_insert)
    return array
    # print(array)

def read_array(array):
    board = [[0 for i in range(9)]for j in range(9)]
    for row in range(len(array)):
        for j in range(81):
            for k in range(81):
                if array[row][k] == 1:
                    for l in range(81, 262):
                        if array[row][l] == 1:
                            board[k//9][k%9] = 1+ l%9
    return board


def cover(item):
    p = node_list[item].dlink.pos
    while p != item:
        hide(p)
        p = node_list[p].dlink.pos
    l = node_list[item].llink.pos
    r = node_list[item].rlink.pos
    node_list[l].rlink = node_list[r]
    node_list[r].llink = node_list[l]


#
# # Hide an option (row)
def hide(pos):
    q = pos+1
    while q != pos:
        j = node_list[q].top
        if j <= 0:
            q = node_list[q].ulink.pos
        else:
            x = node_list[q].top
            u = node_list[q].ulink.pos
            d = node_list[q].dlink.pos
            if x <= 0:
                q = u
            else:
                node_list[u].dlink = node_list[d]
                node_list[d].ulink = node_list[u]
                node_list[x].len = node_list[x].len - 1
                q = q+1

# reinsert an item (column)
def uncover(item):
    l = node_list[item].llink.pos
    r = node_list[item].rlink.pos
    node_list[l].rlink = node_list[item]
    node_list[r].llink = node_list[item]
    p = node_list[item].ulink.pos
    while p!= item:
        unhide(p)
        p = node_list[p].ulink.pos

#reinster an option (column)
def unhide(pos):
    q = pos-1
    while q != pos:
        j = node_list[q].top
        if j <= 0:
            q = node_list[q].dlink.pos
        else:
            x = node_list[q].top
            u = node_list[q].ulink.pos
            d = node_list[q].dlink.pos
            if x <= 0:
                q = d
            else:
                node_list[u].dlink = node_list[q]
                node_list[d].ulink = node_list[q]
                node_list[x].len += 1
                q = q-1




"""
Main solver
"""
"""
12
12, 16 B
20, 24, 9 Solved

"""
def solve_array(array):
    items = len(array[0])
    options = len(array)


    """
    Build Node_List
    """
    global node_list
    # global l

    node_list = []

    new_node = Node(0)
    node_list.append(new_node)

    # add column headers to list
    for j in range(items):
        new_node = Node(j+1)
        new_node.len = 0
        node_list.append(new_node)

    node_list[0].rlink = node_list[1]   #connect header to column headers
    node_list[0].llink = node_list[-1]

    # link headers internally
    for j in range(1, items+1):
        if j == 1:
            node_list[j].llink = node_list[0]
        else:
            node_list[j].llink = node_list[j-1]
        if j == items:
            node_list[j].rlink = node_list[0]
        else:
            node_list[j].rlink = node_list[j+1]

    # insert node objects
    spacer_count = 0 # vertical position of node
    first_spacer = True
    for i in range(options):
        # add spacer
        spacer = len(node_list) # determine global position of node
        new_node = Node(spacer)  # insert row header
        new_node.top = -spacer_count  # give it a negative top index for identification
        new_node.row = i
        spacer_count = spacer_count+1
        node_list.append(new_node)
        node_list[0].len = options  ## give 0-header the longest possible length

        if not first_spacer:
            new_node.ulink = first_node_pointer
        else:
            first_spacer = False

        first_node = True # first node in column
        for j in range(items):  # walk horizontally

            # insert spacer
            if array[i][j] == 1:

                new_node = Node(len(node_list))
                new_node.loc = (i, j)
                new_node.row = i
                new_node.top = j+1           # point to column header
                if node_list[new_node.top].len == 0:   # if first node in column
                    new_node.ulink = node_list[new_node.top]    # stitch up to header
                    node_list[new_node.top].dlink = new_node
                else:
                    count = node_list[new_node.top].len  # number of existing nodes in list
                    last_node_inserted = node_list[new_node.top]
                    while count != 0:       # find last inserted node in column (last_node_inserted)
                        last_node_inserted = last_node_inserted.dlink
                        count = count-1
                    new_node.ulink = last_node_inserted
                    last_node_inserted.dlink = new_node

                if first_node:
                    first_node_pointer = new_node
                first_node = False

                node_list[new_node.top].len += 1
                node_list.append(new_node)

        node_list[spacer].dlink = new_node  # give initial spacer dlink pointer to last node in row

    spacer = len(node_list)
    new_node = Node(spacer)
    new_node.top = -spacer_count
    new_node.ulink = first_node_pointer
    node_list.append(new_node)


    ## connect top and bottom
    for j in range(items):
        search = node_list[j+1].dlink
        if search != None:
            while search.dlink is not None:
                search = search.dlink
            node_list[j+1].ulink = search
            search.dlink = node_list[j+1]


    """

    ## Algorithm ##

    """
    l = 0
    item_list = []
    # removed_list = []
    failed_start = []
    # completed = False
    breakpoint()
    step = 0  # step = {0, 1, or 2}: 0=Try, 1=Try Again, 2=Backtrack
    """
    Pick Item to to try
    """
    # print_data()
    while True:
        # print("l:", l)
        # breakpoint()
        first_shortest_list = 0
        print(step)
        # print_board(item_list, array)
        # check if algorithms completed
        # find first item not in failed items list
        if step == 0:
            # find first remaining option and check if completed
            # breakpoint()
            item_traversal_start = node_list[0].rlink.pos
            if item_traversal_start == 0:  # if completed
                # completed = True
                print("Finished item list:", item_list)
                # convert item list to row locations to return
                # row_list = []
                # position_solution = []
                # solution_ = []   #solution as list
                # solution = []      #solution as 2d array
                # dim = math.floor(math.sqrt(len(solution_)))

                # for i in item_list:  # find position and value
                #     row_list.append(node_list[i].loc[0])
                #     l = node_list[i].loc[0]
                #     for i in range(dim**2):
                #         if array[l][i] == 1:
                #             position = (i//dim, i%dim)
                #         if array[l][2*dim**2+i] == 1:
                #             value = i%dim+1
                #     position_solution.append((position, value))
                #     solution_.append(value)
                # for i in range(dim):
                #     solution.append(solution_[i*4:i*4+4])

                # print(solution_)
                
                return print_board(item_list, array)

            # skip over items that have been tried and failed
            while set(failed_start).__contains__(item_traversal_start):
                item_traversal_start = node_list[item_traversal_start].rlink.pos

            # determine first shortest list remaining to begin search
            i = item_traversal_start
            while i != 0:
                if 0 < node_list[i].len < node_list[first_shortest_list].len:
                    if not set(failed_start).__contains__(i):
                        first_shortest_list = i
                i = node_list[i].rlink.pos
            if first_shortest_list == 0:  #backtrack if shortest list is 0 and not all items filled
                step = 2
            else:
                # print("first_shortest_list found:", first_shortest_list, "len:", node_list[first_shortest_list].len)
                row = node_list[first_shortest_list].dlink.row
                # print(row)
                # print("Starting Choice:", get_item_position(array[node_list[first_shortest_list].dlink.row]))
                # breakpoint()
                if node_list[first_shortest_list].len == 0:  # backtrack if at end of the list
                    step = 2
                else:
                    cover(first_shortest_list)
                    xl = node_list[first_shortest_list].dlink.pos  # find first node below list to remove
                    item_list.append(xl)

        # if proceeding: cover each column covered by xl
        if step == 0:
            # print("trying:", xl)
            p = xl+1
            while p != xl:
                j = node_list[p].top
                if j <= 0:
                    p = node_list[p].ulink.pos
                else:
                    cover(j)
                    p = p+1
            l = l+1

        if step == 1:  # retry
            print("retry")
            p = xl - 1
            # set to backtrack if xl is end of column
            if node_list[xl].top == node_list[xl].dlink.pos:  
                step = 2   # backtrack
            else:          
                while p != xl:    # reinsert option for xl by uncovering each column it covers
                    j = node_list[p].top
                    if j <= 0:
                        p = node_list[p].dlink.pos
                    else:
                        uncover(j)
                        p = p-1

                # pick next element in column
                xl = node_list[xl].dlink.pos
                item_list[-1] = xl
                # print('..retrying:', xl)
                p = xl+1
                while p != xl:
                    j = node_list[p].top
                    if j <= 0:
                        p = node_list[p].ulink.pos
                    else:
                        cover(j)
                        p = p+1
                step = 0

        if step == 2:
            p = xl - 1
            while p != xl:
                j = node_list[p].top
                if j <= 0:
                    p = node_list[p].dlink.pos
                else:
                    uncover(j)
                    p = p-1

            uncover(node_list[xl].top)
            print("end of line:", item_list, l)
            print("failed_start:", failed_start)
            if l == 1:
                failed_start.append(node_list[xl].top)
                if (len(failed_start) == items):
                    print("Process Terminated")
                    break
                item_list = []
                l = 0
                step = 0
            if l == 0:
                step = 0
            else:
                item_list = item_list[:-1]
                xl = item_list[-1]
                l = l-1
                step = 1





def print_data():
    print()
    for i in range(len(node_list)):
        print(node_list[i].pos, node_list[i].len, node_list[i].loc, node_list[i].top)
        if (node_list[i].ulink):
            print('ulink', node_list[i].ulink.pos)
        if (node_list[i].dlink):
            print('dlink', node_list[i].dlink.pos)
    print()


def get_item_position(row):
    dim = math.floor(math.sqrt(len(row)//4)) # get dimension of the board

    for i in range(dim**2):
        if row[i] == 1:
            position = (i//dim, i%dim)
        if row[2*dim**2+i] == 1:
            value = i%dim+1
    return position, value




def print_board(solution, array):
    row_list = [node_list[item].row for item in solution]
    position_value_list = [get_item_position(array[r]) for r in row_list]
    board = [[0 for x in range(9)] for y in range(9)]
    for i in position_value_list:
        r = i[0][0]
        c = i[0][1]
        board[r][c] = i[1]    
    for row in board:
        print(row)
    print("\n")
    return board

# def reduce_array(array, row_list):
    # reduced_array = []
    # for i in row_list:
    #     reduced_array.append(array[i])
    # return reduced_array


# board3x3 = [[2, 0, 0, 0],[0, 1, 0, 2], [0, 0, 3, 0],[0, 0, 0, 4]]
# test_array = transform4x4(board3x3)

t0 = time.time()
array = transform_board(test_board)
solve_array(array)

print(time.time()-t0)
# print(row_list)
# board = read_array(array)
# print(board)
