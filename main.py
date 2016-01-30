#!/usr/bin/python3

from ref import Ref
from gi.repository import Gtk
import display_gui


def init_gui():
    colorRef = Ref(1)
    cubeArea = display_gui.CubeArea(colorRef)
    mainWindow = display_gui.MainWindow()
    colorWindow = display_gui.ColorWindow(colorRef)

    colorWindow.show_all()

    mainWindow.add(cubeArea)
    mainWindow.show_all()


init_gui()

Gtk.main()
