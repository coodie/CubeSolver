import cairo


COLOR_AMOUNT = 7
GREY = 0
WHITE = 1
RED = 2
BLUE = 3
ORANGE = 4
YELLOW = 5
GREEN = 6

'''
Order of colors is listed as:
colors[0] = grey
colors[1] = white
colors[2] = red
colors[3] = blue
colors[4] = orange
colors[5] = yellow
colors[6] = green
'''
colors = [cairo.SolidPattern(0, 0, 0, 0),
          cairo.SolidPattern(1, 1, 1),
          cairo.SolidPattern(153/256, 0, 0),
          cairo.SolidPattern(0, 0, 153/256),
          cairo.SolidPattern(204/256, 102/256, 0),
          cairo.SolidPattern(255, 255, 0),
          cairo.SolidPattern(0, 153/256, 0)]

''' Maps color ints to sides they are associated with '''
color_map = {
    ORANGE: 'B',
    WHITE: 'D',
    BLUE: 'L',
    YELLOW: 'U',
    RED: 'F',
     GREEN: 'R'}

''' Is inversion of color map '''
color_rev_map = {v: k for k, v in color_map.items()}

Uperm = [6, 3, 0, 7, 4, 1, 8, 5, 2,
         45, 46, 47, 12, 13, 14, 15, 16, 17,
         9, 10, 11, 21, 22, 23, 24, 25, 26,
         27, 28, 29, 30, 31, 32, 33, 34, 35,
         18, 19, 20, 39, 40, 41, 42, 43, 44,
         36, 37, 38, 48, 49, 50, 51, 52, 53]

Lperm = [53, 1, 2, 50, 4, 5, 47, 7, 8,
         9, 10, 11, 12, 13, 14, 15, 16, 17,
         0, 19, 20, 3, 22, 23, 6, 25, 26,
         18, 28, 29, 21, 31, 32, 24, 34, 35,
         42, 39, 36, 43, 40, 37, 44, 41, 38,
         45, 46, 33, 48, 49, 30, 51, 52, 27]

Fperm = [0, 1, 2, 3, 4, 5, 44, 41, 38,
         6, 10, 11, 7, 13, 14, 8, 16, 17,
         24, 21, 18, 25, 22, 19, 26, 23, 20,
         15, 12, 9, 30, 31, 32, 33, 34, 35,
         36, 37, 27, 39, 40, 28, 42, 43, 29,
         45, 46, 47, 48, 49, 50, 51, 52, 53]

Rperm = [0, 1, 20, 3, 4, 23, 6, 7, 26,
         15, 12, 9, 16, 13, 10, 17, 14, 11,
         18, 19, 29, 21, 22, 32, 24, 25, 35,
         27, 28, 51, 30, 31, 48, 33, 34, 45,
         36, 37, 38, 39, 40, 41, 42, 43, 44,
         8, 46, 47, 5, 49, 50, 2, 52, 53]

Bperm = [11, 14, 17, 3, 4, 5, 6, 7, 8,
         9, 10, 35, 12, 13, 34, 15, 16, 33,
         18, 19, 20, 21, 22, 23, 24, 25, 26,
         27, 28, 29, 30, 31, 32, 36, 39, 42,
         2, 37, 38, 1, 40, 41, 0, 43, 44,
         51, 48, 45, 52, 49, 46, 53, 50, 47]

Dperm = [0, 1, 2, 3, 4, 5, 6, 7, 8,
         9, 10, 11, 12, 13, 14, 24, 25, 26,
         18, 19, 20, 21, 22, 23, 42, 43, 44,
         33, 30, 27, 34, 31, 28, 35, 32, 29,
         36, 37, 38, 39, 40, 41, 51, 52, 53,
         45, 46, 47, 48, 49, 50, 15, 16, 17]


def get_solved_string():
    return "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"


'''
             |************|
             |*U1**U2**U3*|
             |************|
             |*U4**U5**U6*|
             |************|
             |*U7**U8**U9*|
             |************|
 ************|************|************|************
 *L1**L2**L3*|*F1**F2**F3*|*R1**R2**F3*|*B1**B2**B3*
 ************|************|************|************
 *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
 ************|************|************|************
 *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
 ************|************|************|************
             |************|
             |*D1**D2**D3*|
             |************|
             |*D4**D5**D6*|
             |************|
             |*D7**D8**D9*|
             |************|

Cube is represented as string.
Where at certain positions are colors from cube.
For example string starting with UBL...
means that at U1 position we have U1 color
at U2 position we have B color, at U3
position we have L color and so on.

Positions of colors in string are listed below:

 U1, U2, U3, U4, U5, U6, U7, U8, U9,
 R1, R2, R3, R4, R5, R6, R7, R8, R9,
 F1, F2, F3, F4, F5, F6, F7, F8, F9,
 D1, D2, D3, D4, D5, D6, D7, D8, D9,
 L1, L2, L3, L4, L5, L6, L7, L8, L9,
 B1, B2, B3, B4, B5, B6, B7, B8, B9.

Assuming:
UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
represents soved cube.

Solution notation is the notation used by speedcubers.

Order to define a rotation of face of the cube
it is enough to permute the string in a way
representing specific rotation. Like, doing U
rotation would permute in a way:
F1 -> R1,
R1 -> B1
B1 -> L1
L1 -> F1
... and so on
'''


class Cube():

    def __init__(
        self,
     rep="UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"):
        self.rep = rep

    def get_string(self):
        return self.rep

    ''' Executes sequence of steps on the cube'''

    def execute(self, seq):
        steps = seq.split(" ")
        for move in steps:
            self.one_step(move)

    '''Performs one step, but reversed.
    like instead of doing R', it does R,
    and opposite. '''

    def rev_one_step(self, move):
        if len(move) > 1:
            if(move[1] == "'"):
                self.one_step(move[0:1])
            else:
                self.one_step(move)
        else:
            self.one_step(move+"'")

    '''Performs one step on the cube.
    Some steps can be disassembled into couple
    more base steps like
    R' = R R R,
    R2 = R R
    so it's enough to just define base step
    and use combine them to have more steps.
    '''

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

    '''Performs base step, for which there is direct permutation'''

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

    ''' Applies base permutation '''

    def apply_perm(self, perm):
        old = ""
        for i in range(0, len(perm)):
            old += self.rep[perm[i]]
        self.rep = old
