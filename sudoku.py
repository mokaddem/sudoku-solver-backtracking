import math
import time
import copy

class NxNGrid:
    def __init__(self, arrayNd):
        self.size = len(arrayNd[0])
        self.grid = arrayNd

    def add_digit(self, x, y, digit):
        self.grid[x][y] = digit

    def __repr__(self):
        to_ret = '+---+---+---+\n'
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is None:
                    to_ret += '|   '
                else:
                    to_ret += '| {0['+str(row)+']['+str(col)+']} '
            to_ret += '|\n'
        to_ret += '+---+---+---+\n'
        to_ret = to_ret.format(self.grid)
        return to_ret

    def __str__(self):
        return self.__repr__()

class Sudoku:
    def __init__(self, textfile):
        with open(textfile) as f:
            content = f.read()
        self.grid = Sudoku.parse(content)
        self.size = len(self.grid)
        self.subGridSize = int(math.sqrt(self.size))
        self.subgrids = [[x for x in range(self.subGridSize)] for y in range(self.subGridSize)]
        self.lines = [x for x in range(self.size)]
        self.cols = [x for x in range(self.size)]

        # assign subgrid objects
        for row in range(0, self.size, self.subGridSize):
            for col in range(0, self.size, self.subGridSize):
                subGrid = []
                for subrow in range(row, row+self.subGridSize):
                    row_to_append = self.grid[subrow][col:col+self.subGridSize]
                    subGrid.append(row_to_append)
                self.subgrids[int(row/self.subGridSize)][int(col/self.subGridSize)] = Subgrid(subGrid)

        # assign line objects
        for i, line in enumerate(self.grid):
            self.lines[i] = Line(line)

        # assign column objects
        transposed_grid = [list(i) for i in zip(*self.grid)]
        for i, col in enumerate(transposed_grid):
            self.cols[i] = Column(col)

    def add_digit(self, x, y, digit):
        #update grid
        self.grid[x][y] = digit
        #update subgrid
        subgridNumX = int(x/self.subGridSize)
        subgridNumY = int(y/self.subGridSize)
        subgrid = self.subgrids[subgridNumX][subgridNumY]
        subgrid.add_digit(x % self.subGridSize, y % self.subGridSize, digit)
        #update line
        self.lines[x].add_digit(y, digit)
        #update column
        self.cols[y].add_digit(x, digit)

    def isNone(self, x, y):
        return (self.grid[x][y] is None)

    def isConsistent(self):
        #check lines
        for line in self.lines:
            if not line.isConsistent():
                #print("line not consistent")
                return False
        #check cols
        for col in self.cols:
            if not col.isConsistent():
                #print("column not consistent")
                return False
        #check subgrid
        for subgridX in self.subgrids:
            for subgrid in subgridX:
                if not subgrid.isConsistent():
                    #print("subgrid not consistent")
                    return False
        return True

    def solve(self):
        hints = 0
        for row in self.grid:
            for digit in row:
                if digit is not None:
                    hints += 1
        solved_sudoku = self.backtrackSearch(0, 0, self.size*self.size-hints)

    def __repr__(self):
        to_ret = ('+'+'-'*self.subGridSize)*self.size +'+\n'
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] is None:
                    to_ret += '|'+' '*self.subGridSize
                elif self.grid[row][col]<10:
                    to_ret += '| {0['+str(row)+']['+str(col)+']} ' +' '*int(self.subGridSize/3.1)
                else:
                    to_ret += '| {0['+str(row)+']['+str(col)+']} '
            to_ret += '|\n'
            to_ret += ('+'+'-'*self.subGridSize)*self.size +'+\n'
        to_ret = to_ret.format(self.grid)
        return to_ret

    def __str__(self):
        return self.__repr__()

    def parse(content):
        grid = []
        for line in content.splitlines():
            line = line[1:]
            line = line[:-1]
            lineSplited = line.split(',')
            arrayLine = []
            for num in lineSplited:
                if num == '*':
                    arrayLine.append(None)
                else:
                    arrayLine.append(int(num))
            grid.append(arrayLine)
        return grid

    def backtrackSearch(self, x, y, empties):
        if empties == 0:
            return True

        if self.isConsistent():
            # compute next positions
            nextY = y + 1
            nextX = x
            if nextY == self.size:
                nextY = 0
                nextX = x + 1

            if self.isNone(x, y):
                for testVal in range(1, self.size+1):
                    self.add_digit(x, y, testVal)

                    if self.backtrackSearch(nextX, nextY, empties-1):
                        return True

                    self.add_digit(x, y, None)
            else:
                if self.backtrackSearch(nextX, nextY, empties):
                    return True
        return False


class Subgrid(NxNGrid):
    def isConsistent(self):
        #check lines
        for line in self.grid:
            line = Line(line)
            if not line.isConsistent():
                return False

        #check cols
        transposed_grid = [list(i) for i in zip(*self.grid)]
        for col in transposed_grid:
            col = Column(col)
            if not col.isConsistent():
                return False

        #check subgrid
        numbers = []
        for row in self.grid:
            for digit in row:
                if digit is None:
                    continue
                if digit in numbers:
                    return False
                else:
                    numbers.append(digit)
        return True


class Line(NxNGrid):
    def __init__(self, line):
        self.size = len(line)
        self.grid = line

    def add_digit(self, x, digit):
        self.grid[x] = digit

    def isConsistent(self):
        numbers = []
        for digit in self.grid:
            if digit is None:
                continue
            if digit in numbers:
                return False
            else:
                numbers.append(digit)
        return True


class Column(NxNGrid):
    def __init__(self, column):
        self.size = len(column)
        self.grid = column

    def add_digit(self, y, digit):
        self.grid[y] = digit

    def isConsistent(self):
        numbers = []
        for digit in self.grid:
            if digit is None:
                continue
            if digit in numbers:
                return False
            else:
                numbers.append(digit)
        return True


def main():
    sud = Sudoku("sudo16x16.txt")
    sud = Sudoku("sudo.txt")
    print('Original:')
    print(sud)
    print('Solving...')
    sud.solve()
    print('Solved:')
    print(sud)


if __name__ == "__main__":
    main()
