from typing import Tuple, List, Set, Optional
testcf = 0
imax=0
jmax=0
imin=10
jmin=10
def read_sudoku(filename: str) -> List[List[str]]:
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid
def group(truyen: List[str], n: int) -> List[List[str]]:
    kq=list()
    kq1=list()
    test=0
    for i in range(0,len(truyen)):
        kq1.append(truyen[i])
        if (i+1) % n == 0 :
            kq.append(kq1)
            del(kq1)
            kq1=list()
            
    return kq
def checko(n : int , m : int , truyen: List[str], test: str ):
    tro1=n//3
    tro2=m//3
    for i in range(-2,3,1):
        for j in range(-2,3,1):
            if (n+i)//3 != tro1  or (m+j)//3 != tro2  : 
                continue
            if truyen[n+i][m+j] == test:
                return 0
    return 1
def checkhc(n : int , m : int , truyen: List[str] , test = str):
    for i in range (0,9):
        if truyen[n][i] == test and i!=m:
                return 0
        if truyen[i][m] == test and i!=n:
                return 0
    return 1
def backtracking(truyen: list() ):
    global testcf
    for i in range (0,9):
        for j in range (0,9):
            if truyen[i][j] == '.':
                for k in range (1,10):
                    test=str(k)
                    '''print(i,end=' ' )
                    print(j,end=' ' )
                    print(k)'''
                    if checko(i,j,truyen,test) ==1 and checkhc(i,j,truyen,test) ==1:
                        truyen[i][j]=test
                        if i== imax and j == jmax:
                            testcf=2
                            print(truyen)
                        if testcf == 0 :
                            #print(truyen)
                            backtracking(truyen)
                    if k ==9 and testcf == 0:
                        truyen[i][j]='.'
                        return 
                    if i == 8 and j == 8:
                        exit()
                    if i==imin and j == jmin and testcf ==0 and k==9:
                        testcf=1
def checksol(truyen: list() ):
    global testcf
    if testcf != 2:
        for i in range (0,9):
            for j in range (0,9):
                if truyen[i][j] == '.':
                    if testcf==0:
                        print(f"Puzzle {fname} can't be solved")
                        return 0
    testcf=0
def timmin():
    global imin
    global jmin
    for i in range (0,9):
        for j in range (0,9):
            if grid[i][j] == '.':
                imin=i
                jmin=j
                return
def timmax():
    global imax
    global jmax
    for i in range (8,-1,-1):
        for j in range (8,-1,-1):
            if grid[i][j] == '.':
                    imax=i
                    jmax=j
                    return
for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
    testcf=0
    grid = read_sudoku(fname)
    timmin()
    timmax()
    backtracking(grid)
    checksol(grid)
