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
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight = 1)
        self.resizable(False, False)

        main_container = ttk.Frame(self) # Create a container frame with MainApp as parent
        main_container.grid(column = 0, row = 0, sticky = "nsew") 
        # Put main_container in a MainApp grid (row 0, col 0), sticky N S E W means centered in grid
        main_container.rowconfigure(0, weight = 1) # Configure main_container grid of col 0 with weight 1
        main_container.columnconfigure(0, weight = 1) # Configure main_container grid of row 0 with weight 1

        self.pages = self.get_all_pages(main_container) # Insert all pages into a dictionary main_container is passed by reference
        self.show_page(StartPage) # Start the program by displaying StartPage
    
    def get_all_pages(self, main_container) -> dict: # Function to get all pages and return as dict
        list_of_pages = (StartPage, GamePage) # Add page classes here
        pages = {} # Initialize an empty dict to store pages

        for page in list_of_pages:
            frame = page(main_container, self) # Initializes each page. main_container and MainApp are passed as arguments. 
            pages[page] = frame # The initialized pages are added to pages dictionary with the class objects as their keys
            frame.grid(row = 0, column = 0, sticky = "nsew") # Places each page in main_container grid
        
        return pages

    def show_page(self, page) -> None:
        frame = self.pages[page] # Get the page value (the frame used to display the page)
        frame.tkraise() # Raise the frame so that it's displayed
        return


class StartPage(ttk.Frame):
    def __init__(self, parent, main_app: MainApp):
        super().__init__(parent, relief="solid", padding = (80, 100)) # Initialize StartPage as a child class of ttk.Frame

        game_title = ttk.Label(self, text = "Duolango", justify = "center", font = ("TkDefaultFont", 50))
        game_title.grid(column = 0, row = 0, sticky = "s", columnspan = 3, padx = 5, pady = 5)

        play_button = ttk.Button(self, text = "Play!", command = lambda : main_app.show_page(GamePage))
        play_button.grid(column = 1, row = 1, sticky = "n", padx = 5, pady = 5)

        '''
        self.columnconfigure(0, weight = 1) # reenable if window resizing is going to be implemented
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)
        '''
class GamePage(ttk.Frame):
    def __init__(self, parent, main_app: MainApp):
        super().__init__(parent, relief="solid", padding = (80, 100)) # Initialize StartPage as a child class of ttk.Frame

        game_title = ttk.Label(self, text = "the game", justify = "center", font = ("TkDefaultFont", 50))
        game_title.grid(column = 0, row = 0, sticky = "s", columnspan = 3, padx = 5, pady = 5)

        play_button = ttk.Button(self, text = "asdfasdfasdf!")
        play_button.grid(column = 1, row = 1, sticky = "n", padx = 5, pady = 5)



MainGame = MainApp()
MainGame.mainloop()