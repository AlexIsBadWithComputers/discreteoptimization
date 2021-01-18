
def format_colors(colors):
    '''
    Helper function to adjust output to make the submission
    happy
    '''
    string = ''
    for key, value in sorted(colors.items(), key=lambda x: x[0]): 
        string += str(value) + ' '
    return string

def getDegree(graph):
    '''
    Function to get the degree of a node
    '''
    degree = {}
    for node in graph:
        degree[node] = len(graph[node])
    return degree 

def initializeConstraints(graph):
    '''
    Initialize constraints of each node as an empty set
    '''
    cons = {}
    for node in graph:
        cons[node] = set()
    return cons

def firstFailSort(constraints, visited, graph):
    node_degree = getDegree(graph)
    '''
    Sort for fail first optimization. First sort by the number of constraints, followed by the number of neighbours
    '''
    order = []
    for i in range(len(node_degree)):
        if i not in visited:
            order.append((i, len(constraints[i]), node_degree[i]))
    order.sort(key=lambda x: (x[1], x[2]), reverse=False)

    # get the index
    return [x[0] for x in order]

def getColor(node, graph, constraints, max_colors, temp_constraint):
    '''
    Function to get the color of a node and propogate constraints
    '''
    affected = []
    to_add = []
    
    for color in range(max_colors):
        broken = False
        if (color in constraints[node]) or (color == temp_constraint):
            continue
        else:
            # Set color of current node, 
            # and also add a constraint to its neighbours 
            for n in graph[node]:
                # Only add it if _this_ is the node
                # which is propagating the constraint to it
                if color not in constraints[n]:
                    
                    # If we are selecting the only available
                    # color for a neighbour, select a different
                    # color instead if possible
                    if len(constraints[n]) == max_colors -1:
                        broken = True
                        break
                    else:
                        to_add.append(n) 
            if broken:
                continue  
            for n in to_add:
                 constraints[n].add(color)
                 affected.append(n)
            return color, constraints, None, affected 
    # print(len(constraints[node]), len(graph[node]), 'const')
    return None

def dfs(graph, start, max_colors):
    constraints = initializeConstraints(graph)
    stack = [start]
    visited = set()
    temp_constraint = None
    colors = {}
    visited_order = []
    affected_order = []
    stack = firstFailSort(constraints, visited, graph)
    while stack != []:
      
        node = stack.pop()
        if colors.get(node, False):
            return 
        try:
            int_color, constraints, temp_constraint, affected = getColor(node, graph, constraints, max_colors, temp_constraint)
            colors[node] = int_color
            affected_order.append(affected)
            visited_order.append(node)
            visited.add(node)
        except TypeError:
          
          # So this is meant to do backtracking, but the above scores 
          #  fairly on tests without hitting this, and when it 
          # does hit this, it never seems to stop. So something funky
          # Is happening here I believe  
           
            
            print("I did some backtracking")
            back = visited_order.pop()
            visited.remove(back)
            temp_constraint = colors[back]
            reverse = affected_order.pop()
            for n in reverse:
                constraints[n].remove(colors[back])
            del colors[back]
            continue
            
        
        # Reorder stuff to deal with if this needs to be rearranged
        stack = firstFailSort(constraints, visited, graph)

    return colors, format_colors(colors)






