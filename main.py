'''
Language Game

Google Docs to store stuff: https://docs.google.com/document/d/14FtWRdg6qmq8TTLPX0pCTY7JsXHCW1ZLrHLghgDIbKA/edit?tab=t.0
'''

# import all the libraries..
import tkinter as tk
from tkinter import ttk
import random
import turtle
import time
from copy import deepcopy

# Create tkinter window class
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__() # Initialize MainApp as a child class of tk.Tk
        self.title("Duolango") # Set window title
        self.geometry('960x540')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight = 1)

        self.main_container = ttk.Frame(self) # Create a container frame with MainApp as parent
        self.main_container.grid(column = 0, row = 0, sticky = "nsew") 
        # Put main_container in a MainApp grid (row 0, col 0), sticky N S E W means centered in grid
        self.main_container.rowconfigure(0, weight = 1) # Configure main_container grid of col 0 with weight 1
        self.main_container.columnconfigure(0, weight = 1) # Configure main_container grid of row 0 with weight 1

        self.goto_page(StartPage)
        #self.bind("w", lambda e :self.page.game_canvas.move_forward())
        #print(isinstance(self.page, StartPage))

    def goto_page(self, page_to_goto):
        for child in self.main_container.winfo_children():
            child.destroy()
        self.page = page_to_goto(self.main_container, self)
        self.page.grid(column = 0, row = 0, sticky = "nsew")
        if isinstance(self.page, GamePage):
            self.bind_movement_keys()

    def bind_movement_keys(self):
        self.bind("<KeyPress>", lambda event : self.page.game_canvas.move(event.keysym))
        self.bind("<KeyRelease>", lambda event : self.page.game_canvas.remove_released_keys(event.keysym))

class StartPage(ttk.Frame):
    def __init__(self, parent, main_app: MainApp):
        super().__init__(parent, relief="solid") # Initialize StartPage as a child class of ttk.Frame

        game_title = ttk.Label(self, text = "Duolango", justify = "center", font = ("TkDefaultFont", 50)) # Title
        game_title.grid(column = 0, row = 0, sticky = "s", columnspan = 3, padx = 5, pady = 5) # Place title

        play_button = ttk.Button(self, text = "Play!", command = lambda : main_app.goto_page(GamePage)) # Play button
        play_button.grid(column = 1, row = 1, sticky = "n", padx = 5, pady = 5) # Place play button

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)

class GamePage(ttk.Frame):
    def __init__(self, parent, main_app: MainApp):
        super().__init__(parent, relief = "solid") # Initialize GamePage as a child class of ttk.Frame

        question = ttk.Label(self, text = "qn", justify = "center", font = ("TkDefaultFont", 30))
        question.grid(column = 0, row = 0)
        
        self.game_canvas = GameCanvas(self)
        self.game_canvas.grid(column = 2, row = 0, sticky = "nsew", rowspan = 3)

        info_frame = ttk.Frame(self)
        info_frame.grid(column = 0, row = 2, sticky = "nsew")

        ttk.Separator(self, orient = "horizontal").grid(column = 0, row = 1, sticky = "ew")
        ttk.Separator(self, orient = "vertical").grid(column = 1, row = 0, rowspan = 3, sticky = "ns")

        self.columnconfigure(0, weight = 4)
        self.columnconfigure(2, weight = 5)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(2, weight = 2)
        

# Resizing: https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width

class GameCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, borderwidth = -2) # Initialize GameCanvas as a child class of tk.Canvas
        self.t = turtle.RawTurtle(self) # Initialize a RawTurtle object as a child of GameCanvas
        self.t.penup()
        self.pressed_keys = {"w" : False, "d" : False, "s" : False, "a" : False}
            
    def move(self, pressed_key):
        if pressed_key not in self.pressed_keys:
            return
        self.pressed_keys[pressed_key] = True

        if self.pressed_keys["w"] and self.pressed_keys["s"]:
            self.pressed_keys["w"], self.pressed_keys["s"] = False, False
        if self.pressed_keys["d"] and self.pressed_keys["a"]:
            self.pressed_keys["d"], self.pressed_keys["a"] = False, False
        
        if True not in self.pressed_keys.values():
            return
        if self.pressed_keys["w"] and self.pressed_keys["d"]:
            self.t.setheading(45)
        elif self.pressed_keys["w"] and self.pressed_keys["a"]:
            self.t.setheading(135)
        elif self.pressed_keys["s"] and self.pressed_keys["a"]:
            self.t.setheading(225)
        elif self.pressed_keys["s"] and self.pressed_keys["d"]:
            self.t.setheading(315)
        elif self.pressed_keys["w"]:
            self.t.setheading(90)
        elif self.pressed_keys["a"]:
            self.t.setheading(180)
        elif self.pressed_keys["s"]:
            self.t.setheading(270)
        elif self.pressed_keys["d"]:
            self.t.setheading(0)
        self.t.forward(10)
        return
    
    def remove_released_keys(self, released_key):
        if released_key not in self.pressed_keys:
            return
        self.pressed_keys[released_key] = False
        return

MainGame = MainApp()
#MainGame.bind("w", lambda w: MainGame.pages[GamePage].game_canvas.move_forward()) # error
MainGame.mainloop()