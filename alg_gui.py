from gi.repository import Gtk
from gi.repository import Gdk

import display_gui
import cube
import solver

class StepDisplayer(Gtk.Box):
    X_SIZE = 100
    Y_SIZE = 100

    def __init__(self):
        super(StepDisplayer, self).__init__()
        self.image = Gtk.Image.new()
        self.pack_start(self.image, True, True, 6)
        self.set_size_request(StepDisplayer.X_SIZE, StepDisplayer.Y_SIZE)

    def set_step(self, step):
        step = step.replace("'", "p")
        self.image.set_from_file("./images/"+step+".gif")
        self.set_size_request(StepDisplayer.X_SIZE, StepDisplayer.Y_SIZE)
        self.show()

class AlgWindow(Gtk.Window):
    X_SIZE = 300
    Y_SIZE = 200

    def __init__(self, cubeArea):
        super(AlgWindow, self).__init__()
        self.set_title("")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(AlgWindow.X_SIZE, AlgWindow.Y_SIZE)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        button_box = Gtk.Box(spacing=3)
        box = Gtk.ListBox()

        button = Gtk.Button.new_with_label("Find Solution")
        button.connect("clicked", self.solve_button)
        button_box.pack_start(button, True, True, 6)

        button = Gtk.Button.new_with_label("Next")
        button.connect("clicked", self.next_button)
        button_box.pack_start(button, True, True, 6)

        button = Gtk.Button.new_with_label("Prev")
        button.connect("clicked", self.prev_button)
        button_box.pack_start(button, True, True, 6)

        self.text_displayer = Gtk.TextView()
        self.text_displayer.set_editable(False)
        self.step_displayer = StepDisplayer()

        box.insert(self.step_displayer, -1)
        box.insert(self.text_displayer, -1)
        box.insert(button_box, -1)
        self.add(box)

        self.cubeArea = cubeArea
        self.solving = False
        self.steps = [""]
        self.cur_step = 0

    def display_text(self, msg):
        self.text_displayer.get_buffer().set_text(msg)

    def display_step(self, i):
        if i < len(self.steps) and i >= 0:
            self.step_displayer.set_step(self.steps[i])

    def solve_button(self, button):
        self.solving = True
        c = self.cubeArea.get_cube()
        try:
            steps = solver.solve(c.get_string())
            self.display_text(steps)
            self.steps = steps.split(" ")
            self.cur_step = 0
            self.display_step(self.cur_step)
        except ValueError:
            self.display_text("Invalid cube scramble")
            self.solving = False

    def prev_button(self, button):
        if self.solving:
            c = self.cubeArea.get_cube()
            if self.cur_step > 0:
                self.cur_step = self.cur_step-1
                c.rev_one_step(self.steps[self.cur_step])

                self.display_step(self.cur_step)
                self.cubeArea.from_cube(c)
                self.cubeArea.queue_draw()

    def next_button(self, button):
        if self.solving:
            c = self.cubeArea.get_cube()
            if self.cur_step < len(self.steps):
                c.one_step(self.steps[self.cur_step])
                self.cur_step = self.cur_step+1
                self.display_step(self.cur_step)
                self.cubeArea.from_cube(c)
                self.cubeArea.queue_draw()




