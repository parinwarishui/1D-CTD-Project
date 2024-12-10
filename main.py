'''
Language Game

Google Docs to store stuff: https://docs.google.com/document/d/14FtWRdg6qmq8TTLPX0pCTY7JsXHCW1ZLrHLghgDIbKA/edit?tab=t.0
'''

# import all the libraries..
import tkinter as tk
from tkinter import ttk
import random
import turtle
import os
from copy import deepcopy
import winsound
import time

# Create tkinter window class
class MainApp(tk.Tk):
    '''Main App where the pages are placed'''
    def __init__(self):
        super().__init__() # Initialize MainApp as a child class of tk.Tk
        self.title("Duolango") # Set window title
        self.geometry('540x540') # Set initial screen size
        self.resizable(False, False) # Disable resizing
        self.rowconfigure(0, weight = 1) # Control size of main frame widget within the window
        self.columnconfigure(0, weight = 1)

        self.main_container = ttk.Frame(self) # Create a container frame with MainApp as parent
        # Put main_container in a MainApp grid (row 0, col 0), sticky N S E W means centered in grid
        self.main_container.grid(column = 0, row = 0, sticky = "nsew", padx = 0, pady = 0) 
        self.main_container.rowconfigure(0, weight = 1) # Configure main_container grid of col 0 with weight 1
        self.main_container.columnconfigure(0, weight = 1) # Configure main_container grid of row 0 with weight 1

        self.get_high_score() # Load high scores from high_score.txt
        self.goto_page(StartPage) # Go to title page


    def goto_page(self, target_page, language = None, inf_mode = False):
        '''Function to go to a specific page'''
        winsound.PlaySound(None, winsound.SND_PURGE) # Stop all sounds currently playing
        winsound.PlaySound("assets/button_click.wav", winsound.SND_FILENAME|winsound.SND_ASYNC) # Play button click sound
                                                                                                # SND_ASYNC allows code to run
                                                                                                # while sound is playing
        for child in self.main_container.winfo_children(): # Get all frames under main container
            child.destroy() # Destroy each frame
        time.sleep(0.2) # Pause 0.2s for sound (to avoid conflict with next winsound.PlaySound)
        if target_page == GamePage or target_page == InfiniteGamePage: # If target page is one of the two types of game pages
            self.page = target_page(self.main_container, self, language) # Instantiates self.page as an object of type target_page
        else:
            self.page = target_page(self.main_container, self) # Same as above, but without language being passed

        self.page.grid(column = 0, row = 0, sticky = "nsew", padx = 0, pady = 0) # Puts the page into main_container grid

        x = int(self.winfo_screenwidth()/2 - self.page.window_size[0]/2) # Gets x coordinates to put window
        y = int(self.winfo_screenheight()/2 - self.page.window_size[1]/2 - 32) # Gets y coordinates to put window
                                                                               # -32 is to compensate for title bar
        # Resize window & centerize (syntax: "xsize x ysize + x + y")
        self.geometry("{}x{}+{}+{}".format(self.page.window_size[0], self.page.window_size[1], x, y))

        if isinstance(self.page, GamePage): # Checks if self.page is an instance of GamePage (including inherited classes)
            self.bind_movement_keys() # Runs the bind_movement_keys function
        else: # If self.page is not an instance of GamePage (if self.page is a StartPage)
            self.unbind_movement_keys() # Runs the unbind_movement_keys function

    def bind_movement_keys(self):
        """
        Function to bind movement keys to self.page.game_canvas.move function
        This function is only called if the target page is GamePage or a child of GamePage
        """
        # Bind key press & release events to game_canvas.move function
        # passes event.keysym (contains pressed buttons as str type) as argument
        self.bind("<KeyPress>", lambda event : self.page.game_canvas.move(event.keysym, self.page, self))
        self.bind("<KeyRelease>", lambda event : self.page.game_canvas.remove_released_keys(event.keysym))
    
    def unbind_movement_keys(self):
        """
        Function to unbind movement keys to avoid getting warnings when pressing keys on StartPage
        """
        self.unbind("<KeyPress>")
        self.unbind("<KeyRelease>")

    def get_high_score(self):
        '''Function to get high score of each language file from txt files'''
        if not os.path.exists("assets/high_score.txt"): # Checks if high_score.txt does not exist
           open("assets/high_score.txt", 'a').close # Create a new high_score.txt file

        with open("assets/high_score.txt", "r") as f: # Open the high score txt file in read mode
            lines = f.readlines() # assign list of every line to lines
            # Read all lines and put high scores into language:score dictionary format
            self.high_scores = {lang.strip():score.strip() for lang, score in [line.split(":") for line in lines]}

    def update_highscore(self, new_high_score, language):
        """
        Updates high_score.txt
        This code only runs after the player gets a new high score
        """
        self.high_scores[language] = new_high_score # Changes the high score value for the assigned language
        with open("assets/high_score.txt", "w+") as f: # Rewrites high_score.txt with updated high score values
            for language, score in self.high_scores.items():
                f.write("{}:{}\n".format(language, score))

class StartPage(tk.Frame):
    '''Starting Page (Title + Play buttons)'''
    def __init__(self, parent, main_app: MainApp):
        super().__init__(parent, relief="solid") # Initialize StartPage as a child class of ttk.Frame
        self.window_size = (540, 540) # Sets window size for StartPage

        winsound.PlaySound("assets/title.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP) # Plays title music

        game_title = ttk.Label(self, text = "Duolango", justify = "center", font = ("Cooper Black", 50), foreground = "green") # Title label
        game_title.grid(column = 0, row = 0, sticky = "s", columnspan = 4, padx = 5, pady = 0) # Place title label

        available_languages = os.listdir("words_lists") # Creates list of all files (& directories) at words_lists folder
        available_languages.append("Add another language") # Adds the option to add another language
        self.language_choice = tk.StringVar() # Creates a variable self.language_choice to store Combobox choice
        self.language_combobox = ttk.Combobox(self, textvariable = self.language_choice, state = "readonly", values = available_languages)
        self.language_combobox.grid(column = 1, row = 3, columnspan = 2, pady = 5) # Places combobox
        self.language_combobox.bind("<<ComboboxSelected>>", lambda e : choose_language()) # Runs choose_language() if a selection is made

        self.play_button = tk.Button(self, text = "   Play Game   ", command = lambda : main_app.goto_page(GamePage, self.language_choice.get()), 
                                 relief = "raised", font = ("gothic", 11, "bold"), height = 1, state = "disabled", 
                                 background = "gray64", foreground = "gray32") # Play button
        self.play_button.grid(column = 1, row = 2, sticky = "n", padx = 2, pady = 5) # Place play button

        self.learn_button = tk.Button(self, text = " Learning Mode ", command = lambda : main_app.goto_page(InfiniteGamePage, self.language_choice.get()), 
                                 relief = "raised", font = ("gothic", 11, "bold"), height = 1, state = "disabled",
                                 background = "gray64", foreground = "gray32") # Learning mode button
        self.learn_button.grid(column = 2, row = 2, sticky = "n", padx = 2, pady = 5) # Place learning mode button
        
        self.score_str = tk.StringVar(self, "High Score: {}".format("--")) # Creates a string variable to store high score text
        highscore_label = ttk.Label(self, textvariable = self.score_str, justify = "center", font = ("fixedsys", 13))
        highscore_label.grid(column = 1, row = 1, columnspan = 2, sticky = "n", pady = 3) # Places highscore label
        
        self.refresh_button = tk.Button(self, text = " Refresh ", command = lambda : update_combobox(), 
                                 relief = "raised", font = ("gothic", 11), height = 1) # Creates a refresh button (but not placed)
        
        # Configuring sizes to make start page look neat
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(5, weight = 4)

        def choose_language():
            '''Function that runs when a combobox selection is made'''
            if self.language_choice.get() == "Add another language": # If selection is to add another language
                # Disable buttons (+ visuals)
                self.learn_button["foreground"] = "gray32"
                self.learn_button["background"] = "gray64"
                self.learn_button["state"] = "disabled"
                self.play_button["foreground"] = "gray32"
                self.play_button["background"] = "gray64"
                self.play_button["state"] = "disabled"
                
                self.refresh_button.grid(column = 1, row = 4, columnspan = 2, pady = 0) # Shows refresh button
                self.score_str.set("High Score: {}".format("--")) # Sets high score to -- (since no language has been chosen)
                
                with open("words_lists/RenameToLanguageName.txt", "w+") as f: # Creates a new txt file
                                                                              # w+ means read and write mode
                    # Writes instructions & examples
                    f.write("#Enter your words along with their translations here!\n")
                    f.write("#You can look at the other pre-made txt files for reference\n")
                    f.write("#Don't forget to rename this file to whatever name you want for this deck!\n")
                    f.write("#P.S. The game requires at least 4 words before it can run properly\n")
                    f.write("#Feel free to remove these instructions after you're done editing\n")
                    f.write("word1:meaning1\n")
                    f.write("word2:meaning2\n")
                    f.write("word3:meaning3\n")
                    f.write("word4:meaning4\n")
                main_app.update() # Update the app (so combobox shows new selection)
                self.after(500) # Pauses the program for 500 ms
                script_dir = os.path.dirname(__file__) # Gets directory of main.py file
                os.startfile(os.path.realpath(os.path.join(script_dir, "words_lists"))) # Opens words_lists folder
                os.startfile(os.path.join(script_dir, "words_lists/RenameToLanguageName.txt")) # Opens newly made txt file

            else: # if selection is an already available language
                # Enables buttons (+ visuals)
                self.learn_button["foreground"] = "gray3" 
                self.learn_button["background"] = "gray95"
                self.learn_button["state"] = "normal"
                self.play_button["foreground"] = "gray3"
                self.play_button["background"] = "gray95"
                self.play_button["state"] = "normal"

                self.refresh_button.grid_forget() # Hides refresh button
                # Updates the score_str variable to match the selected language's high score
                self.score_str.set("High Score: {}".format(int(main_app.high_scores.get(self.language_choice.get(), 0))))

        def update_combobox():
            '''Function that runs when reset button is pressed'''
            available_languages = os.listdir("words_lists") # Lists all files in words_lists folder
            available_languages.append("Add another language") # Adds option to add another language
            self.language_combobox["values"] = available_languages # Updates values of combobox with current available languages

class GameCanvas(tk.Canvas):
    '''Class for game canvas, mainly used for turtle'''
    def __init__(self, parent, main_app:MainApp):
        self.canvas_width = 670 # Set canvas_width for future use
        self.canvas_height = 540 # Set canvas_height for future use
        super().__init__(parent, border = 0, highlightthickness = 0, width = self.canvas_width-80, 
                         height = self.canvas_height) # Initialize GameCanvas as a child class of tk.Canvas
        self.configure(bg = "black") # Set background of canvas to black color
        
        self.init_game(parent) # Initialize the game

    def init_game(self, parent):
        '''Function to initialize the game, only called once'''
        self.screen = turtle.TurtleScreen(self) # Create a TurtleScreen for turtle objects
        self.t = turtle.RawTurtle(self.screen) # Initialize a RawTurtle object as a child of the turtle screen
                                               # RawTurtle is used since turtle is running in embedded mode
        self.configure(bg = "black") # Set background of gamecanvas to black (since creating a turtle screen clears 
                                     # the current screen
        self.configure(scrollregion = (0, int(self.__getitem__("height")), int(self.__getitem__("width")), 0))
        # Configure viewable part of canvas (Syntax: Left, Top, Right, Bottom)

        # Create the main playable turtle
        self.t.shape("turtle")
        self.t.color("green4")
        self.t.penup()
        self.t.speed(0)
        self.t.shapesize(3,3,1)
        self.pressed_keys = {} # Create an empty dictionary to store keyboard keys that are being pressed

        self.textbox_positions = [(90, -50), (self.canvas_width-90, -50), (90, 50-self.canvas_height), 
                                  (self.canvas_width-90, 50-self.canvas_height)] # List of positions for placing options
        self.textboxes = [] # List to store textbox turtle objects
        for pos in self.textbox_positions: # Initialize the text boxes
            textbox = turtle.RawTurtle(self.screen)
            textbox.penup()
            textbox.color("white")
            textbox.speed(0)
            textbox.hideturtle()
            textbox.goto(pos)
            self.textboxes.append(textbox)

        self.question_display = turtle.RawTurtle(self.screen) # Creates a RawTurtle object for displaying questions
        self.question_display.hideturtle()
        self.question_display.penup()
        self.question_display.color("white")
        self.question_display.goto(self.canvas_width/2, 75-self.canvas_height/2)

        self.lives = 3 # Initializes the amount of lives to 3
        self.questions_list = self.get_all_questions(parent) # Gets all questions and stores them in a list
        self.available_questions = deepcopy(self.questions_list) # Creates a deepcopy of the list to store the available
                                                                 # (unused) questions
        random.shuffle(self.available_questions) # Shuffle the available questions

        self.init_round() # Initialize the 1st round

    def init_round(self):
        '''Function to initialize each round'''
        self.t.goto(self.canvas_width/2, -self.canvas_height/2) # Centerize
        self.t.setheading(90) # Facing upwards
        self.load_questions()
        self.question_display.clear()        
        self.question_display.write(self.question["question"], align = "center", font=("Arial", 15, "bold"))
        self.show_questions()
        self.pressed_keys = {"w" : False, "d" : False, "s" : False, "a" : False} # Initializing keys for movement

    def move(self, pressed_key, parent, main_app):
        if pressed_key not in self.pressed_keys:
            return
        self.pressed_keys[pressed_key] = True
        
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

        self.boundary_check()
        self.collision_check(parent, main_app)
        return
    
    def remove_released_keys(self, released_key):
        if released_key not in self.pressed_keys:
            return
        self.pressed_keys[released_key] = False
        return

    def boundary_check(self):
        if self.t.xcor() > self.canvas_width:
            self.t.setx(self.canvas_width)
        elif self.t.xcor() < 0:
            self.t.setx(0)
        if self.t.ycor() < -self.canvas_height:
            self.t.sety(-self.canvas_height)
        elif self.t.ycor() > 0:
            self.t.sety(0)
    
    def collision_check(self, parent, main_app: MainApp):
        for box_num, textbox in enumerate(self.textboxes):
            if self.t.distance(textbox) < 60:
                self.pressed_keys.clear() # Stop movement
                correct = True if self.options[box_num] == self.question else False
                
                if not correct:
                    self.lives -= 1
                    parent.update_lives(self.lives)
                    if self.lives <= 0:
                        self.end_game(parent, main_app)
                        return
                else:
                    parent.update_score()

                for box_num, (textbox, option) in enumerate(zip(self.textboxes, self.options)):
                    textbox.color(("lawn green" if self.options[box_num] == self.question else "red"))
                    textbox.clear()
                    textbox.write(option["answer"], align = "center", font = ("Arial", 12, "normal"))

                self.after(1000)
                self.init_round()
                

    def get_all_questions(self, parent):
        with open(("words_lists/{}".format(parent.language)), 'r', encoding = "utf8") as f: # utf8 encoding is used to handle some characters
            questions = [dict(zip(("question", "answer"), map(lambda s:s.strip(), (line.split(":"))))) for line in f if ":" in line and line[0] != "#"]
        return questions

    def load_questions(self):
        if len(self.available_questions) <= 0:
            self.available_questions = deepcopy(self.questions_list)
            random.shuffle(self.available_questions)
        self.question = self.available_questions.pop()

        options_count = 0
        self.options = []
        possible_options = deepcopy(self.questions_list)
        random.shuffle(possible_options)
        while (options_count < 3):
            possible_option = possible_options.pop()
            if possible_option != self.question:
                self.options.append(possible_option)
                options_count += 1
        self.options.append(self.question)
        random.shuffle(self.options)
    
    def show_questions(self):
        for textbox, option in zip(self.textboxes, self.options):
            textbox.color("white")
            textbox.clear()
            textbox.write(option["answer"], align = "center", font = ("Arial", 12, "normal"))

    def end_game(self, parent, main_app: MainApp):
        winsound.PlaySound(None, winsound.SND_PURGE)

        if parent.score > int(main_app.high_scores.get(parent.language, 0)) and parent.inf_mode == False:
            main_app.update_highscore(parent.score, parent.language)
        
        # Turtle dying animation
        self.screen.resetscreen()
        self.t.shape("turtle")
        self.t.color("green4")
        self.t.penup()
        self.t.speed(0)
        self.t.shapesize(3,3,1)
        self.t.goto(self.canvas_width/2, -self.canvas_height/2)
        self.t.setheading(90)
        self.after(500)
        self.t.speed(1)
        self.t.right(180)
        self.screen.delay(20)

        winsound.PlaySound("assets/death.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP)

        self.after(500)
        self.t.forward(200)
        self.after(500)
        self.t.left(90)
        self.after(500)
        self.t.color("light grey")
        self.screen.delay(10) # Return delay to default value

        self.after(1000)
        ttk.Label(self, text = "You Lose!", background = "black", foreground = "white", justify = "center", 
                  font = ("Comic Sans MS", 50)).place(relx = 0.5, rely = 0.2, anchor = "center")
        main_app.update()
        self.after(1000)
        ttk.Label(self, text = "Final Score: {}".format(parent.score), background = "black", foreground = "white", 
                  justify = "center", font = ("Comic Sans MS", 20)).place(relx = 0.5, rely = 0.325, anchor = "center")
        main_app.update()
        self.after(1000)
        home_button = tk.Button(self, text = "    Home    ", background = "light grey", foreground = "black", 
                                justify = "center", font = ("Comic Sans MS", 15), relief = "raised", 
                                command = lambda: main_app.goto_page(StartPage))
        home_button.place(relx = 0.4, rely = 0.44, anchor = "center")
        main_app.update()
        self.after(300)
        again_button = tk.Button(self, text = " Play Again ", background = "light grey", foreground = "black", 
                                justify = "center", font = ("Comic Sans MS", 15), relief = "raised", 
                                command = lambda: main_app.goto_page(GamePage, parent.language))
        again_button.place(relx = 0.6, rely = 0.44, anchor = "center")
        main_app.update()

class InfiniteGameCanvas(GameCanvas):
    def collision_check(self, parent, main_app: MainApp): # Same as GameCanvas but no punishment if wrong ans
        for box_num, textbox in enumerate(self.textboxes):
            if self.t.distance(textbox) < 60:
                self.pressed_keys.clear() # Stop movement
                correct = True if self.options[box_num] == self.question else False
                for box_num, (textbox, option) in enumerate(zip(self.textboxes, self.options)):
                    textbox.color(("lawn green" if self.options[box_num] == self.question else "red"))
                    textbox.clear()
                    textbox.write(option["answer"], align = "center", font = ("Arial", 12, "normal"))
                self.after(1000)
                if correct:
                    parent.update_score()
                self.init_round()

class GamePage(ttk.Frame):
    def __init__(self, parent, main_app: MainApp, language, canvas_type = GameCanvas, inf_mode = False):
        super().__init__(parent, relief = "solid",borderwidth = 0) # Initialize GamePage as a child class of ttk.Frame
        winsound.PlaySound("assets/game_music.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_LOOP)
        self.window_size = (960,540)
        self.inf_mode = inf_mode
        self.language = language

        self.info_frame = ttk.Frame(self)
        self.info_frame.grid(column = 0, row = 0)
        self.score = 0
        self.scoreStr = tk.StringVar(self, "Score:{}".format(self.score))
        score_label = ttk.Label(self.info_frame, textvariable = self.scoreStr, justify = "center", font = ("fixedsys", 30))
        score_label.grid(column = 0, row = 1, padx = 0, pady = 0, columnspan = 2)
        
        self.game_canvas = canvas_type(self, main_app)
        self.game_canvas.grid(column = 2, row = 0, sticky = "nsew", rowspan = 3, padx = 0, pady = 0)

        self.lives_images = {3:"assets/3hearts.png", 2: "assets/2hearts.png", 1: "assets/1hearts.png", 0: "assets/0hearts.png"}
        self.lives_image = tk.PhotoImage(file = self.lives_images[3])
        self.lives_label = ttk.Label(self, image = self.lives_image, justify = "center")
        self.lives_label.grid(column = 0, row = 2)

        ttk.Separator(self, orient = "horizontal").grid(column = 0, row = 1, sticky = "ew", pady = 0)
        ttk.Separator(self, orient = "vertical").grid(column = 1, row = 0, rowspan = 3, sticky = "ns", padx = 0)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 5)
        self.rowconfigure(2, weight = 2)
    
    def update_score(self):
        self.score += random.randint(1, 3)*10
        self.scoreStr.set("Score: {}".format(self.score))
        return

    def update_lives(self, lives):
        self.lives_image = tk.PhotoImage(file = self.lives_images[lives])
        self.lives_label.config(image = self.lives_image)
        return

class InfiniteGamePage(GamePage):
    def __init__(self, parent, main_app: MainApp, language):
        super().__init__(parent, main_app, language, canvas_type = InfiniteGameCanvas, inf_mode = True)
        self.lives_image = tk.PhotoImage(file = "assets/infhearts.png")
        self.lives_label.config(image = self.lives_image)
        
        self.info_frame.grid(column = 0, row = 0, sticky = "nsew")
        tk.Button(self.info_frame, text = "Back", background = "light grey", foreground = "black", 
                                justify = "left", font = ("TkDefaultFont", 10), relief = "ridge", borderwidth = 2, 
                                command = lambda: main_app.goto_page(StartPage)).grid(column = 0, row = 0, sticky = "nw", padx = 0, pady = 0)
        self.info_frame.columnconfigure(0, weight = 1)
        self.info_frame.columnconfigure(1, weight = 1)
        self.info_frame.rowconfigure(0, weight = 1)
        self.info_frame.rowconfigure(1, weight = 1)
        self.info_frame.rowconfigure(2, weight = 1)

MainGame = MainApp()
MainGame.mainloop()