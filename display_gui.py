from gi.repository import Gtk
from gi.repository import Gdk
import cube


class MainWindow(Gtk.Window):
    X_SIZE = 600
    Y_SIZE = 450

    def __init__(self):
        super(MainWindow, self).__init__()
        self.set_title("Kostka")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(MainWindow.X_SIZE, MainWindow.Y_SIZE)
        self.set_position(Gtk.WindowPosition.CENTER)


def gen_33_grid(x, y):
    return [(x0, y0) for x0 in [x, x+1, x+2] for y0 in [y, y+1, y+2]]


class CubeArea(Gtk.DrawingArea):
    tile_x = MainWindow.X_SIZE//12
    tile_y = MainWindow.Y_SIZE//9
    blocked_tiles = set(
        [(10, 4), (4, 4), (1, 4), (7, 4), (4, 7), (4, 1)] +
        gen_33_grid(0, 0) + gen_33_grid(6, 0) + gen_33_grid(9, 0) +
        gen_33_grid(0, 6) + gen_33_grid(6, 6) + gen_33_grid(9, 6))

    def __init__(self, colorRef):
        super(CubeArea, self).__init__()

        self.grid_init()
        self.colorRef = colorRef

        self.connect('draw', self.draw)

        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.mouse_click)

    def grid_init(self):
        self.grid = [[0 for _ in range(0, 3*3)] for _ in range(0, 3*4)]

        st = cube.Cube()
        self.from_cube(st)
        # self.fill_square(9, 3, cube.WHITE)
        # self.fill_square(3, 3, cube.YELLOW)
        # self.fill_square(0, 3, cube.BLUE)
        # self.fill_square(6, 3, cube.GREEN)
        # self.fill_square(3, 6, cube.RED)
        # self.fill_square(3, 0, cube.ORANGE)

    def from_cube(self, cube):
        st = cube.get_string()
        self.str_to_square(st[0:9], 3, 0)
        self.str_to_square(st[9:18], 6, 3)
        self.str_to_square(st[18:27], 3, 3)
        self.str_to_square(st[27:36], 3, 6)
        self.str_to_square(st[36:45], 0, 3)
        self.str_to_square(st[45:54], 9, 3)

    def get_cube(self):
        res = ''
        res = res + self.square_to_str(3, 0)
        res = res + self.square_to_str(6, 3)
        res = res + self.square_to_str(3, 3)
        res = res + self.square_to_str(3, 6)
        res = res + self.square_to_str(0, 3)
        res = res + self.square_to_str(9, 3)
        return cube.Cube(res)

    def str_to_square(self, st, x, y):
        k = 0
        for i in range(y, y+3):
            for j in range(x, x+3):
                self.grid[j][i] = cube.color_rev_map[st[k]]
                k = k+1

    def square_to_str(self, x, y):
        res = ''
        for i in range(y, y+3):
            for j in range(x, x+3):
                res = res + cube.color_map[self.grid[j][i]]
        return res

    def fill_square(self, x, y, col):
        for i in range(x, x+3):
            for j in range(y, y+3):
                self.grid[i][j] = col

    def draw(self, _, cr):

        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(3)

        for i in range(0, len(self.grid)):
            x0 = CubeArea.tile_x*i
            for j in range(0, len(self.grid[i])):
                y0 = CubeArea.tile_y*j
                # print(x0,y0)
                cr.set_source(cube.colors[self.grid[i][j]])
                cr.rectangle(x0+2, y0+2, CubeArea.tile_x-4, CubeArea.tile_y-4)
                cr.fill()
                if(not (i, j) in CubeArea.blocked_tiles):
                    cr.set_source_rgb(0, 0, 0)
                    cr.move_to(x0, y0)
                    cr.line_to(x0+CubeArea.tile_x, y0)
                    cr.line_to(x0+CubeArea.tile_x, y0+CubeArea.tile_y)
                    cr.line_to(x0, y0+CubeArea.tile_y)
                    cr.line_to(x0, y0)
                    cr.stroke()

    def mouse_click(self, _, e):
        x, y = int(e.x), int(e.y)
        x //= CubeArea.tile_x
        y //= CubeArea.tile_y
        if((x, y) in CubeArea.blocked_tiles):
            return

        if(e.button == 1):
            self.grid[x][y] = self.colorRef.val
        else:
            c = self.get_cube()
            c.solve()
            self.from_cube(c)

        self.queue_draw()


class ColorWindow(Gtk.Window):
    X_SIZE = CubeArea.tile_x*1
    Y_SIZE = CubeArea.tile_x*7

    def __init__(self, colorRef):
        super(ColorWindow, self).__init__()
        self.set_title("Kolor")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(ColorWindow.X_SIZE, ColorWindow.Y_SIZE)
        self.show_all()

        self.colorRef = colorRef

        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.mouse_click)

        self.area = Gtk.DrawingArea()
        self.area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.area.connect('button-press-event', self.mouse_click)
        self.area.connect('draw', self.draw)
        self.add(self.area)

    def draw(self, _, cr):
        cr.set_source(cube.colors[self.colorRef.val])
        cr.rectangle(0, 0, CubeArea.tile_x, CubeArea.tile_y)
        cr.fill()
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(5)
        cr.move_to(0, CubeArea.tile_y)
        cr.line_to(ColorWindow.X_SIZE, CubeArea.tile_y)
        cr.stroke()
        for i in range(1, cube.COLOR_AMOUNT):
            cr.set_source(cube.colors[i])
            cr.rectangle(0, i*CubeArea.tile_y, CubeArea.tile_x, CubeArea.tile_y)
            cr.fill()

    def mouse_click(self, _, e):
        x, y = int(e.x), int(e.y)
        x //= CubeArea.tile_x
        y //= CubeArea.tile_y

        if (y > 0):
            self.colorRef.val = y

        self.area.queue_draw()
