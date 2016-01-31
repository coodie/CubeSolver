from gi.repository import Gtk
from gi.repository import Gdk

import display_gui
import cube
import solver

class AlgWindow(Gtk.Window):
    X_SIZE = 300
    Y_SIZE = 200

    def __init__(self, cubeArea):
        super(AlgWindow, self).__init__()
        self.set_title("")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(AlgWindow.X_SIZE, AlgWindow.Y_SIZE)
        self.set_position(Gtk.WindowPosition.CENTER)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.Button.new_with_label("Solve")
        button.connect("clicked", self.solve_button)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_label("Next")
        button.connect("clicked", self.next_button)
        hbox.pack_start(button, True, True, 0)

        self.cubeArea = cubeArea
        self.solving = False
        self.steps = [""]
        self.cur_step = 0


    def solve_button(self, button):
        self.solving = True
        c = self.cubeArea.get_cube()
        try:
            steps = solver.solve(c.get_string())
            self.steps = steps.split(" ")
        except ValueError:
            print("Invalid cube scramble")
            self.solving = False
        self.cur_step = 0

    def next_button(self, button):
        if self.solving:
            c = self.cubeArea.get_cube()
            if self.cur_step < len(self.steps):
                c.one_step(self.steps[self.cur_step])
                self.cur_step = self.cur_step+1
                self.cubeArea.from_cube(c)
                self.cubeArea.queue_draw()
            else:
                self.solving = False








