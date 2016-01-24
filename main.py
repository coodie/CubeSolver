#!/usr/bin/python3

from gi.repository import Gtk
from gi.repository import Gdk
import cairo
import random


class GCube():
    COLOR_AMOUNT = 7
    GREY = 0
    WHITE = 1
    RED = 2
    BLUE = 3
    ORANGE = 4
    YELLOW = 5
    GREEN = 6
    colors = [cairo.SolidPattern(0,0,0,0),            # szary
            cairo.SolidPattern(1,1,1),                # bialy
            cairo.SolidPattern(153/256,0,0),          # czerwony
            cairo.SolidPattern(0,0,153/256),          # niebieski
            cairo.SolidPattern(204/256,102/256,0),    # pomaranczowy
            cairo.SolidPattern(255,255,0),            # zolty
            cairo.SolidPattern(0,153/256,0)           # zielony
            ]

    def __init__(self):
        arr =   [[[ 0 for _ in range(0,3)]
                    for _ in range(0,3)]
                        for _ in range (0,6)]
        arr[0][1][1] = GCube.BLUE
        arr[1][1][1] = GCube.ORANGE
        arr[2][1][1] = GCube.WHITE
        arr[3][1][1] = GCube.GREEN
        arr[4][1][1] = GCube.RED
        arr[5][1][1] = GCube.YELLOW


class MainWindow(Gtk.Window):
    X_SIZE = 600
    Y_SIZE = 450
    def __init__(self):
        super(MainWindow, self).__init__()
        self.set_title("Kostka")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(MainWindow.X_SIZE, MainWindow.Y_SIZE)
        self.set_position(Gtk.WindowPosition.CENTER)


def gen_33_grid(x,y):
    return [(x0,y0) for x0 in [x,x+1,x+2] for y0 in [y,y+1,y+2] ]

class CubeArea(Gtk.DrawingArea):

    tile_x = MainWindow.X_SIZE//12
    tile_y = MainWindow.Y_SIZE//9
    blocked_tiles = set(
        [(10, 4), (4, 4), (1, 4), (7, 4), (4, 7), (4, 1)] +
        gen_33_grid(0,0) + gen_33_grid(6,0) + gen_33_grid(9,0) +
        gen_33_grid(0,6) + gen_33_grid(6,6) + gen_33_grid(9,6) )



    def __init__(self):
        super(CubeArea, self).__init__()

        self.grid_init()

        self.connect('draw', self.draw)

        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.mouse_click)

    def grid_init(self):
        self.grid = [ [ 0 for _ in range(0,3*3) ] for _ in range (0,3*4) ]
        self.grid[10][4] = GCube.WHITE
        self.grid[4][4] = GCube.YELLOW
        self.grid[1][4] = GCube.BLUE
        self.grid[7][4] = GCube.GREEN
        self.grid[4][7] = GCube.RED
        self.grid[4][1] = GCube.ORANGE

    def draw(self, w, cr):

        cr.set_source_rgb(0,0,0)
        cr.set_line_width(3)

        for i in range(0, len(self.grid)):
            x0 = CubeArea.tile_x*i
            for j in range(0, len(self.grid[i])):
                y0 = CubeArea.tile_y*j
                # print(x0,y0)
                cr.set_source(GCube.colors[self.grid[i][j]])
                cr.rectangle(x0+2,y0+2,CubeArea.tile_x-4,CubeArea.tile_y-4)
                cr.fill()
                if( not (i,j) in CubeArea.blocked_tiles):
                    cr.set_source_rgb(0,0,0)
                    cr.move_to(x0,y0)
                    cr.line_to(x0+CubeArea.tile_x,y0)
                    cr.line_to(x0+CubeArea.tile_x,y0+CubeArea.tile_y)
                    cr.line_to(x0,y0+CubeArea.tile_y)
                    cr.line_to(x0,y0)
                    cr.stroke()

    def next_col(self,x,y):
        self.grid[x][y] += 1
        self.grid[x][y] %= GCube.COLOR_AMOUNT
        if(self.grid[x][y] == 0):
            self.next_col(x,y)

    def prev_col(self,x,y):
        self.grid[x][y] = (self.grid[x][y]-1 + GCube.COLOR_AMOUNT) % GCube.COLOR_AMOUNT
        if(self.grid[x][y] == 0):
            self.prev_col(x,y)

    def mouse_click(self,_,e):
        x,y = int(e.x),int(e.y)
        x //= CubeArea.tile_x
        y //= CubeArea.tile_y
        if((x,y) in CubeArea.blocked_tiles): return
        if(e.button == 1):
            self.next_col(x,y)
        else:
            self.prev_col(x,y)

        self.queue_draw()








def init_gui():
    area = CubeArea()
    mainWindow = MainWindow()
    mainWindow.add(area)
    mainWindow.show_all()


init_gui()

Gtk.main()
