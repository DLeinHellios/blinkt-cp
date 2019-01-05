#!/usr/bin/env python3
# A simple Tk GUI color picker for the Pimoroni Blinkt for Raspberry Pi | By Dylan Lein-Hellios (https://github.com/dleinhellios)
#   Requires Python 3, Tkinter, and official Blinkt library (https://github.com/pimoroni/blinkt)

from tkinter import *
import blinkt, sys


class Handler:
    '''Reads values from sliders and handles setting pixels'''
    def __init__(self):
        self.values = [0,0,0,0]


    def set(self, s, p):
        # Accepts settings and pixel objects determines selected pixels and passes displayed settings
        self.values = [s.red.get(), s.green.get(), s.blue.get(), s.bright.get()]
        for n, pixel in p.pixelValues.items():
            if pixel.get():
                blinkt.set_pixel(int(n),self.values[0],self.values[1],self.values[2],self.values[3])


    def show(self,s,p):
        # Sets values with set method, then displays
        self.set(s,p)
        blinkt.show()


class Panels:
    '''Panels for GUI construction'''
    def __init__(self, master):
        self.settingsFrame = Frame(padx = 5)
        self.menuFrame = Frame(padx = 5)
        self.pixelFrame = Frame(padx = 10)
        self.place()


    def place(self):
        self.settingsFrame.grid(row = 1, column = 2)
        self.menuFrame.grid(row = 2, column = 2, sticky = E)
        self.pixelFrame.grid(row = 1, column = 1, rowspan = 2)


class Settings:
    '''Displays Red, Green, Blue, and Brightness sliders'''
    def __init__(self, master):
        self.red = Scale(master, from_=255, to=0, fg = 'red')
        self.green = Scale(master, from_=255, to=0, fg = 'green')
        self.blue = Scale(master, from_=255, to=0, fg = 'blue')
        self.bright = Scale(master, from_=1.0, to=0, resolution = .1)
        self.labelRed = Label(master, text = "Red", fg = 'red')
        self.labelGreen = Label(master, text = "Green", fg = 'green')
        self.labelBlue = Label(master, text = "Blue", fg = 'blue')
        self.labelBright = Label(master, text = "Bright")
        self.bright.set(.2) # Sets slider to Blinkt default brightness
        self.place()


    def place(self):
        # Labels
        self.labelRed.grid(row = 1, column = 1)
        self.labelGreen.grid(row = 1, column = 2)
        self.labelBlue.grid(row = 1, column = 3)
        self.labelBright.grid(row = 1, column = 4)

        # Sliders
        self.red.grid(row = 2, column = 1)
        self.green.grid(row = 2, column = 2)
        self.blue.grid(row = 2, column = 3)
        self.bright.grid(row = 2, column = 4)


class Menu:
    '''Displays menu buttons (show, clear, exit)'''
    def __init__(self, master, settings, pixels, handler):
        self.clear = Button(master, text = "Clear", command = self.command_clear)
        self.show = Button(master, text = "Show", command = lambda: handler.show(settings, pixels))
        self.exit = Button(master, text = "Exit", command = self.command_exit)
        self.place()


    def place(self):
        self.exit.pack(side = RIGHT)
        self.clear.pack(side = RIGHT)
        self.show.pack(side = RIGHT)


    def command_clear(self):
        # Turns off all pixels
        blinkt.clear()
        blinkt.show()


    def command_exit(self):
        # Exit application
        blinkt.clear()
        blinkt.show()
        sys.exit()


class Pixels:
    '''Displays pixel selection checkboxes'''
    def __init__(self, master):
        self.allValue = BooleanVar()
        self.allButton= Checkbutton(master, text = "All ", variable = self.allValue, command = self.set_all)
        self.pixelButtons = {}
        self.pixelValues = {}
        for pixel in range(8):
            self.pixelValues[str(pixel)] = BooleanVar()
            self.pixelButtons[str(pixel)] = Checkbutton(master, text = "P:" + str(pixel), variable = self.pixelValues[str(pixel)], command = self.reset_all)
        self.allButton.invoke()
        self.place()


    def place(self):
        self.allButton.grid(row = 1)
        for n, pixel in self.pixelButtons.items():
            pixel.grid(row = 2 + int(n))


    def set_all(self):
        # Command for "All" checkbutton
        for n, pixel in self.pixelButtons.items():
            if self.allValue.get():
                pixel.select()
            else:
                pixel.deselect()


    def reset_all(self):
        # Unchecks "all" button if one pixel is turned off
        for n, pixel in self.pixelValues.items():
            if pixel.get() == False:
                self.allButton.deselect()


def init_root_window():
    '''Configure root Tk() window'''
    root = Tk()
    root.title("blinkt-cp")
    root.resizable(False, False)
    return root


def init_window_contents(master, handler):
    '''Configure UI elements'''
    panels = Panels(master)
    settings = Settings(panels.settingsFrame)
    pixels = Pixels(panels.pixelFrame)
    menu = Menu(panels.menuFrame, settings, pixels, handler)


def main():
    root = init_root_window()
    handler = Handler()
    init_window_contents(root, handler)
    root.mainloop()


if __name__ == "__main__":
    main()
