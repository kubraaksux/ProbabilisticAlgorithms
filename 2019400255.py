import numpy as np
import math
import time
import sys

class ChessboardGame():

    def __init__(self,prob,chessboard_length, count, outputFile):
        self.chessboard_length = chessboard_length 
        self.chessboard_size = chessboard_length* chessboard_length
        self.minVisit = math.ceil(prob*self.chessboard_size)
        
        self.outputFile = outputFile
        self.count = count
        self.initializeGameboard()



    def initializeGameboard(self):
        #initialize chessboard
        self.chessboard = np.empty([self.chessboard_length,self.chessboard_length],dtype=int)
        self.chessboard.fill(-1)

        self.current_pos = np.random.randint(0,self.chessboard_length,(2), dtype=int) #initial position of the knight
        self.current_move = 0
        self.move(0,0) #initial move, change the value in the chessboard to 0
        if self.outputFile is not None :
            self.outputFile.write("Run {}: starting from ({},{})\n".format(self.count, self.current_pos[0], self.current_pos[1]))


        self.all_moves = np.array([[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]],dtype=int) #all moves for the knight
        

    def printGameboard(self):
        # self.printCurrentPosition()
        # print(self.chessboard)
        if self.outputFile is not None :
            self.outputFile.write(str(self.chessboard)+"\n\n")

    def printCurrentPosition(self):
        print("Current Position: ",self.current_pos[0],self.current_pos[1])
        print("Current Move: ",self.current_move)

    def move(self,x,y):
        self.current_pos[0] = self.current_pos[0]+x
        self.current_pos[1] = self.current_pos[1]+y


        #print to outputfile
        if self.outputFile is not None :
            self.outputFile.write("Stepping into ({},{})\n".format(self.count, self.current_pos[0], self.current_pos[1]))
        
        self.chessboard[self.current_pos[0],self.current_pos[1]] = self.current_move
        self.current_move+=1
    
    def unmove(self,x,y):
        #do the reverse of move operation(backtracking)
        self.chessboard[self.current_pos[0],self.current_pos[1]] = -1
        self.current_pos[0] = self.current_pos[0]-x
        self.current_pos[1] = self.current_pos[1]-y
        self.current_move-=1
    


    def findAvailableSquares(self):
        available_moves = []
        for one_move in self.all_moves:
            new_pos = self.current_pos + one_move
            if(new_pos[0]>=0 and new_pos[0]<self.chessboard_length and new_pos[1]>=0 and new_pos[1]<self.chessboard_length and self.chessboard[new_pos[0],new_pos[1]]==-1):
                available_moves.append(one_move)
        return available_moves
        



    def runChessboardGame(self):
        
        while(self.current_move < self.minVisit):
            available_moves = self.findAvailableSquares()
            if(len(available_moves)==0):
                #we are stuck, dead end
                return False,self.current_move
            else:
                next_move = np.random.randint(0,len(available_moves))
                self.move(available_moves[next_move][0],available_moves[next_move][1])

        return True,self.current_move #visited the minimum number of squares

    def runKRandomChessboardGame(self, k):

        if(k!=0):
            while(k>0):
                available_moves = self.findAvailableSquares()
                if(len(available_moves)==0):
                    #we are stuck, dead end// actually it is not possible
                    k = 0
                    return False
                else:
                    next_move = np.random.randint(0,len(available_moves))
                    self.move(available_moves[next_move][0],available_moves[next_move][1])
                k-=1

        if(self.current_move >= self.minVisit):
            return True
        
        for i in range(len(self.all_moves)):
            
            row, col = self.current_pos[0] + self.all_moves[i][0], self.current_pos[1] + self.all_moves[i][1]
            if(row>=0 and row<self.chessboard_length and col>=0 and col<self.chessboard_length and self.chessboard[row,col]==-1):
                self.move(self.all_moves[i][0],self.all_moves[i][1])
                if self.runKRandomChessboardGame(k):
                    return True
        
                #backtracking
                self.unmove(self.all_moves[i][0],self.all_moves[i][1])

        return False
      


if __name__ == "__main__":

	# total arguments
    n = len(sys.argv)

    if(n<2):
        print("You should give a parameter for part 1 or part 2 execution!")
        sys.exit()
    elif n > 2:
        print("You gave more than one parameter!")
        sys.exit()
	 
    # Arguments passed
    if sys.argv[1].strip()!="part1" and sys.argv[1].strip()!="part2":
        print("You should give the parameter as 'part1' or 'part2'!")
        sys.exit()

    firstOneBool = True if sys.argv[1]=="part1" else False

    probs = [0.7,0.8,0.85]
    chessboard_length = 8
    count = 0
    trials = 100000
    kValues = [0,2,3]

    ##execution_times = {}

    if firstOneBool:
        for prob in probs:
            successful_tours = 0
            count = 0
            with open("results_{}.txt".format(prob), "w") as outputFile:
                while count < trials:
                    game = ChessboardGame(prob, chessboard_length, count, outputFile)
                    success, tour_length = game.runChessboardGame()
                    if success:
                        outputFile.write("Successful - Tour length: {}\n".format(tour_length))
                        successful_tours += 1
                    else:
                        outputFile.write("Unsuccessful - Tour length: {}\n".format(tour_length))

                    game.printGameboard()
                    count += 1
                ##end_time = time.time() 
                ##total_time = end_time - start_time
                ##execution_times[prob] = end_time - start_time
                print("LasVegas Algorithm With p = {}".format(prob))
                print("Number of successful tours: {}".format(successful_tours))
                print("Number of trials: {}".format(trials))
                print("Probability of a successful tour: {}\n".format(successful_tours/trials))

                ##print("Total Time of Execution: {:.2f} seconds\n".format(execution_times[prob]))

    

    else:
        for prob in probs:
            for k in kValues:
                print(kValues)
                successful_tours = 0
                count = 0
                #start_time = time.time() 
                
                while count < trials:
                    game = ChessboardGame(prob, chessboard_length, count, None)
                    success = game.runKRandomChessboardGame(k)
                    if success:
                        successful_tours += 1

                    count += 1

                #end_time = time.time()  
                #total_time = end_time - start_time  

                print("--- p = {} ---".format(prob))
                print("LasVegas Algorithm With p = {}, k = {}".format(prob, k))
                print("Number of successful tours: {}".format(successful_tours))
                print("Number of trials: {}".format(trials))
                print("Probability of a successful tour: {}\n".format(successful_tours/trials))
                #print("Total Time of Execution for p = {}, k = {}: {:.2f} seconds\n".format(prob, k, total_time))
                print()



