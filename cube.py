import cairo


COLOR_AMOUNT = 7
GREY = 0
B = WHITE = 1
D = RED = 2
L = BLUE = 3
U = ORANGE = 4
F = YELLOW = 5
R = GREEN = 6
color_map = ['X', 'B', 'D', 'L', 'U', 'F', 'R']
colors = [cairo.SolidPattern(0, 0, 0, 0),            # szary
          cairo.SolidPattern(1, 1, 1),                # bialy
          cairo.SolidPattern(153/256, 0, 0),          # czerwony
          cairo.SolidPattern(0, 0, 153/256),          # niebieski
          cairo.SolidPattern(204/256, 102/256, 0),    # pomaranczowy
          cairo.SolidPattern(255, 255, 0),            # zolty
          cairo.SolidPattern(0, 153/256, 0)]          # zielony
