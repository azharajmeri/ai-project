from django.shortcuts import render

from django.http import JsonResponse
from django.forms.models import model_to_dict

from collections import deque
from copy import deepcopy

# Create your views here.
def home(request):
    return render(request, 'index.html')

def solverView(request, data):
    if request.method == 'POST':

        class EightPuzzel:
            def __init__(self, state, parent, move, level):
                self.state = state
                self.parent = parent
                self.level = level
                self.move = move
                self.stringstate = ' '.join([str(i) for i in state])

        def usingBFS(initialState, goalState):
            queue = deque([EightPuzzel(initialState, None, None, 0)])
            explored = set()
            while len(queue) > 0:
                currentState = queue.popleft()
                explored.add(currentState.stringstate)

                if currentState.state == goalState:
                    return currentState

                nodes, movement = findAllMoves(currentState)
                print(nodes )
                for i in range(0, len(nodes)):
                    statestring = ' '.join([str(i) for i in nodes[i]])
                    if statestring not in explored:
                        queue.append(EightPuzzel(nodes[i], currentState, movement[i], currentState.level+1))

            return False


        def indexFinder(myList):
            for i in range(0, 3):
                for j in range(0, 3):
                    if(myList[i][j] == 0):
                        return (i, j)


        def findAllMoves(parentState):
            indexs = indexFinder(parentState.state)
            indexi = indexs[0]
            indexj = indexs[1]

            leftMove = None
            rightMove = None
            topMove = None
            bottomMove = None

            listOfMoves = []
            moves = []

            if(indexj != 0): #Left
                leftMove = deepcopy(parentState.state)
                leftMove[indexi][indexj] = leftMove[indexi][indexj-1]
                leftMove[indexi][indexj-1] = 0
                listOfMoves.append(leftMove)
                moves.append('Moved '+str(leftMove[indexi][indexj])+' to Right')

            if(indexj != 2): #Right
                rightMove = deepcopy(parentState.state)
                rightMove[indexi][indexj] = rightMove[indexi][indexj+1]
                rightMove[indexi][indexj+1] = 0
                listOfMoves.append(rightMove)
                moves.append('Moved '+str(rightMove[indexi][indexj])+' to Left')

            if(indexi != 0):
                topMove = deepcopy(parentState.state)
                topMove[indexi][indexj] = topMove[indexi-1][indexj]
                topMove[indexi-1][indexj] = 0
                listOfMoves.append(topMove)
                moves.append('Moved '+str(topMove[indexi][indexj])+' to Bottom')

            if(indexi != 2):
                bottomMove = deepcopy(parentState.state)
                bottomMove[indexi][indexj] = bottomMove[indexi+1][indexj]
                bottomMove[indexi+1][indexj] = 0
                listOfMoves.append(bottomMove)
                moves.append('Moved '+str(bottomMove[indexi][indexj])+' to Top')

            return (listOfMoves, moves)




        goalState = [[0, 1, 2], 
                    [3, 4, 5],
                    [6, 7, 8]]
                    
        initialState = [[1, 2, 5],
                        [3, 4, 8], 
                        [6, 7, 0]]
        k = 0
        for i in range(0, 3):
            for j in range(0, 3):
                initialState[i][j] = int(data[k])
                k+=1

        result = usingBFS(initialState, goalState)
        if result != False:
            parent = result.parent
            Sequence = ""
            if parent != None:
                while True:
                    temp=""
                    for i in parent.state:
                        for j in i:
                            temp += str(j)
                    Sequence = temp + Sequence
                    if parent.parent != None:
                        parent = parent.parent
                    else:
                        temp = ""
                        for i in result.state:
                            for j in i:
                                temp += str(j)
                            
                        Sequence = Sequence + temp
                        break
        else:
            temp = ""
            for i in result.state:
                for j in i:
                    temp += str(j)
                
            Sequence = Sequence + temp

            print(Sequence)

        return JsonResponse({'solution': Sequence}, status=200)
    return render(request, 'index.html')