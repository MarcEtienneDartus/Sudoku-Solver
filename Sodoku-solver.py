from __future__ import print_function
import sys
import random
from ortools.sat.python import cp_model

def main(gridSize,chunkSize,startingGrid,limitSolution,returnGrid,printResult):
  model = cp_model.CpModel()
  # Creates the variables.
  # The array index is the columnRange, and the value is the row.
  lineRange = range(0,gridSize)
  columnRange = range(0,gridSize)
  chunkRange =  range(0,chunkSize)
  grid = {}
  for line in lineRange:
    for column in columnRange:
      grid[line,column] = model.NewIntVar(1, gridSize, 'cell %i %i' % (line,column))

      
  # AllDifferent sur les lignes
  for line in lineRange:
    lineDiference = []
    for column in columnRange:
      lineDiference.append(grid[line, column])
    model.AddAllDifferent(lineDiference)

    
  # AllDifferent sur les colonnes
  for column in columnRange:
    columnDiference = []
    for line in lineRange:
      columnDiference.append(grid[line, column])
    model.AddAllDifferent(columnDiference)

  # AllDifferent sur les chunks
  for chunkline in chunkRange:
    for chunkcolumn in chunkRange:
      chunck = []
      for positionline in chunkRange:
        for positioncolumn in chunkRange:
          chunck.append(grid[chunkline * chunkSize + positionline, chunkcolumn * chunkSize + positioncolumn])
      model.AddAllDifferent(chunck)

  # Initial values.
  for line in lineRange:
    for column in columnRange:
      if startingGrid[line][column]>0:
        model.Add(grid[line, column] == startingGrid[line][column])
  
  solver = cp_model.CpSolver()
  if(returnGrid):
    status = solver.Solve(model)
    solution = []
    if status == cp_model.FEASIBLE:
        for line in lineRange:
          lineList=[]
          for column in columnRange:
            lineList.append(int(solver.Value(grid[line,column])))
          solution.append(lineList)
    return solution
  else:
    solution_printer = SolutionPrinter(grid,limitSolution,printResult)
    solver.SearchForAllSolutions(model, solution_printer)
    if(printResult):
      print()
      print('Number of solution: '+str(solution_printer.SolutionCount()))
    return solution_printer.SolutionCount()

def GenerateSudoku(size,chunck,difficulty):
  grid = [[0 for x in range(size)] for y in range(size)]
  possibleValue = list(range(1, size+1))
  random.shuffle(possibleValue)
  for index in range(size):
    grid[index][index] = possibleValue[index]
  completeGrid = main(size,chunck,grid,0,True,False)
  nbCell = 0
  if(difficulty == '1'):
    nbCell = 64
  elif(difficulty == '2'):
    nbCell = 55
  elif(difficulty == '3'):
    nbCell = 48
  elif(difficulty == '4'):
    nbCell = 41
  else:
    nbCell = 31
  print(nbCell)
  for index in range(nbCell):
    DeleteValue(completeGrid,size)
  print('Grid to fill :')
  return completeGrid

def CopyGrid(grid,size):
  newGrid=[]
  for line in range(size):
    lineList=[]
    for column in range(size):
      lineList.append(grid[line][column])
    newGrid.append(lineList)
  return newGrid

def DeleteValue(grid,size):
  x = random.randint(0, size-1)
  y = random.randint(0, size-1)
  if(grid[x][y]!=0):
    newGrid = CopyGrid(grid,size)
    newGrid[x][y] = 0
    solution = main(size,int(size**0.5),newGrid,1,True,False)
    if(len(solution) > 0):
      grid[x][y] = 0
    else:
      DeleteValue(grid,size)
  else:
    DeleteValue(grid,size)

def PrintGrid(grid,size):
  for line in range(size):
    for column in range(size):
      print(grid[line][column],end=' ')
    print()
  


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, grid,limitSolution,printResult):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.grid = grid
    self.limitSolution = limitSolution
    self.printResult = printResult
    self.solutionCount = 0

  def OnSolutionCallback(self):
    self.solutionCount += 1
    if(self.printResult):
      print('Solution '+ str(self.solutionCount))
      gridRange = range(int(len(self.grid)**(.5)))
      for line in gridRange:
          for column in gridRange:
            print(self.Value(self.grid[line,column]), end=' ')
          print()
      print()
      if(self.solutionCount >= self.limitSolution):
        print('Stop: the number of solution reach the limit  ' + str(self.limitSolution))
        self.StopSearch()

  def SolutionCount(self):
    return self.solutionCount
    
if __name__ == '__main__':
  gridSize = 9
  chunkSize = 3
  print("Difficulty:")
  print("1 - Very Hard")
  print("2 - Hard")
  print("3 - Medium")
  print("4 - Easy")
  print("5 - Beginner")
  difficulty = input("Choice:")
  startingGrid = GenerateSudoku(gridSize,chunkSize,difficulty)
  PrintGrid(startingGrid,gridSize)
  main(gridSize,chunkSize,startingGrid,10,False,True)
  