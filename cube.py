import cairo
import copy
import solver


COLOR_AMOUNT = 7
GREY = 0
WHITE = 1
RED = 2
BLUE = 3
ORANGE = 4
YELLOW = 5
GREEN = 6


color_map =     { 1 : 'B', 2 : 'D', 3 : 'L', 4 : 'U', 5 : 'F', 6 : 'R'}
color_rev_map = {'B' : 1, 'D' : 2, 'L' : 3, 'U' : 4, 'F' : 5, 'R' : 6 }

colors = [cairo.SolidPattern(0, 0, 0, 0),            # szary
          cairo.SolidPattern(1, 1, 1),                # bialy
          cairo.SolidPattern(153/256, 0, 0),          # czerwony
          cairo.SolidPattern(0, 0, 153/256),          # niebieski
          cairo.SolidPattern(204/256, 102/256, 0),    # pomaranczowy
          cairo.SolidPattern(255, 255, 0),            # zolty
          cairo.SolidPattern(0, 153/256, 0)]          # zielony

#       [0,1,2,3,4,5,6,7,8,
#        9,10,11,12,13,14,15,16,17,
#        18,19,20,21,22,23,24,25,26,
#        27,28,29,30,31,32,33,34,35,
#        36,37,38,39,40,41,42,43,44,
#        45,46,47,48,49,50,51,52,53]

Uperm = [6, 3, 0, 7, 4, 1, 8, 5, 2,
         45,46,47,12,13,14,15,16,17,
         9, 10,11,21,22,23,24,25,26,
         27,28,29,30,31,32,33,34,35,
         18,19,20,39,40,41,42,43,44,
         36,37,38,48,49,50,51,52,53]

Lperm = [53, 1, 2, 50, 4, 5, 47, 7, 8,
         9, 10,11,12,13,14,15,16,17,
         0,19,20,3,22,23,6,25,26,
         18,28,29,21,31,32,24,34,35,
         42,39,36,43,40,37,44,41,38,
         45,46,33,48,49,30,51,52,27]

Fperm = [0, 1, 2, 3, 4, 5, 44, 41, 38,
         6, 10,11,7,13,14,8,16,17,
         24,21,18,25,22,19,26,23,20,
         15,12,9,30,31,32,33,34,35,
         36,37,27,39,40,28,42,43,29,
         45,46,47,48,49,50,51,52,53]

Rperm = [0, 1, 20, 3, 4, 23, 6, 7, 26,
         15, 12,9,16,13,10,17,14,11,
         18,19,29,21,22,32,24,25,35,
         27,28,51,30,31,48,33,34,45,
         36,37,38,39,40,41,42,43,44,
         8,46,47,5,49,50,2,52,53]

Bperm = [11, 14, 17, 3, 4, 5, 6, 7, 8,
         9, 10,35,12,13,34,15,16,33,
         18,19,20,21,22,23,24,25,26,
         27,28,29,30,31,32,36,39,42,
         2,37,38,1,40,41,0,43,44,
         51,48,45,52,49,46,53,50,47]

Dperm = [0, 1, 2, 3, 4, 5, 6, 7, 8,
         9, 10,11,12,13,14,24,25,26,
         18,19,20,21,22,23,42,43,44,
         33,30,27,34,31,28,35,32,29,
         36,37,38,39,40,41,51,52,53,
         45,46,47,48,49,50,15,16,17]

def get_solved_string():
    return "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

class Cube():
    B = WHITE -1
    D = RED   -1
    L = BLUE  -1
    U = ORANGE-1
    F = YELLOW-1
    R = GREEN -1


    def __init__(self, rep ="UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"):
        self.rep = rep

    def get_string(self):
        return self.rep


    def apply_perm(self, perm):
        old = ""
        for i in range(0,len(perm)):
            old += self.rep[perm[i]]
        self.rep = old

    def solve(self):
        print(self.rep)
        steps = solver.solve(self.rep)
        print(steps)
        self.execute(steps)


    def execute(self, seq):
        steps = seq.split(" ")
        for move in steps:
            self.one_step(move)

    def one_step(self, move):
        base = move[0]
        if len(move) > 1:
            if move[1] == "'":
                self.base_step(base)
                self.base_step(base)
                self.base_step(base)
            if move[1] == "2":
                self.base_step(base)
                self.base_step(base)
        else:
            self.base_step(move)

    def base_step(self, move):
        if move == "B":
            self.apply_perm(Bperm)
        elif move == "D":
            self.apply_perm(Dperm)
        elif move == "L":
            self.apply_perm(Lperm)
        elif move == "U":
            self.apply_perm(Uperm)
        elif move == "F":
            self.apply_perm(Fperm)
        elif move == "R":
            self.apply_perm(Rperm)
        else:
            raise ValueError("Unknown move: " + move)
