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
        self.geometry('540x540')
        self.resizable(False, False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight = 1)

        self.main_container = ttk.Frame(self) # Create a container frame with MainApp as parent
        self.main_container.grid(column = 0, row = 0, sticky = "nsew", padx = 0, pady = 0) 
        # Put main_container in a MainApp grid (row 0, col 0), sticky N S E W means centered in grid
        self.main_container.rowconfigure(0, weight = 1) # Configure main_container grid of col 0 with weight 1
        self.main_container.columnconfigure(0, weight = 1) # Configure main_container grid of row 0 with weight 1

        self.goto_page(StartPage)

    def goto_page(self, target_page):
        for child in self.main_container.winfo_children():
            child.destroy()
        self.page = target_page(self.main_container, self)
        self.page.grid(column = 0, row = 0, sticky = "nsew", padx = 0, pady = 0)

        x = int(self.winfo_screenwidth()/2 - self.page.window_size[0]/2)
        y = int(self.winfo_screenheight()/2 - self.page.window_size[1]/2 - 32)
        self.geometry("{}x{}+{}+{}".format(self.page.window_size[0], self.page.window_size[1], x, y))

        if isinstance(self.page, GamePage):
            self.bind_movement_keys()
        else:
            self.unbind_movement_keys()

    def bind_movement_keys(self):
        self.bind("<KeyPress>", lambda event : self.page.game_canvas.move(event.keysym, self.page, self))
        self.bind("<KeyRelease>", lambda event : self.page.game_canvas.remove_released_keys(event.keysym))
    
    def unbind_movement_keys(self):
        self.unbind("<KeyPress>")
        self.unbind("<KeyRelease>")

class StartPage(tk.Frame):
    def __init__(self, parent, main_app: MainApp):
        super().__init__(parent, relief="solid") # Initialize StartPage as a child class of ttk.Frame
        self.window_size = (540, 540)

        game_title = ttk.Label(self, text = "Duolango", justify = "center", font = ("TkDefaultFont", 50)) # Title
        game_title.grid(column = 0, row = 0, sticky = "s", columnspan = 4, padx = 5, pady = 5) # Place title

        play_button = ttk.Button(self, text = "   Play Game   ", command = lambda : main_app.goto_page(GamePage)) # Play button
        play_button.grid(column = 1, row = 1, sticky = "n", padx = 0, pady = 5) # Place play button

        learn_button = ttk.Button(self, text = " Learning Mode ", command = lambda : main_app.goto_page(InfiniteGamePage)) # Play button
        learn_button.grid(column = 2, row = 1, sticky = "n", padx = 0, pady = 5) # Place play button

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)

class GameCanvas(tk.Canvas):
    def __init__(self, parent, main_app:MainApp):
        self.canvas_width = 670
        self.canvas_height = 540
        # Initialize GameCanvas as a child class of tk.Canvas
        super().__init__(parent, border = 0, highlightthickness = 0, 
                         width = self.canvas_width-80, height = self.canvas_height) 
        self.configure(bg = "black")
        
        self.init_game()

    def init_game(self):
        self.screen = turtle.TurtleScreen(self)
        self.t = turtle.RawTurtle(self.screen) # Initialize a RawTurtle object as a child of GameCanvas
        self.configure(bg = "black")

        self.configure(scrollregion = (0, int(self.__getitem__("height")), int(self.__getitem__("width")), 0))
                                    #  Left, Top, Right, Bottom
        self.t.shape("turtle")
        self.t.color("green4")
        self.t.penup()
        self.t.speed(0)
        self.t.shapesize(3,3,1)
        self.pressed_keys = {}

        self.textbox_positions = [(80, -50), (self.canvas_width-80, -50), (80, 50-self.canvas_height), (self.canvas_width-80, 50-self.canvas_height)]
        self.textboxes = []
        for pos in self.textbox_positions: # Initialize the text boxes
            textbox = turtle.RawTurtle(self.screen)
            textbox.penup()
            textbox.color("white")
            textbox.speed(0)
            textbox.hideturtle()
            textbox.goto(pos)
            self.textboxes.append(textbox)
        self.question_display = turtle.RawTurtle(self.screen)
        self.question_display.hideturtle()
        self.question_display.penup()
        self.question_display.color("white")
        self.question_display.goto(self.canvas_width/2, 75-self.canvas_height/2)

        self.lives = 3
        # self.draw_border()
        self.questions_list = self.get_all_questions()
        self.available_questions = deepcopy(self.questions_list)
        random.shuffle(self.available_questions)
        
        self.init_round()

    def init_round(self):
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
        print(int(self.t.xcor()), int(self.t.ycor()))

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
                for box_num, (textbox, option) in enumerate(zip(self.textboxes, self.options)):
                    textbox.color(("lawn green" if self.options[box_num] == self.question else "red"))
                    textbox.clear()
                    textbox.write(option["answer"], align = "center", font = ("Arial", 12, "normal"))
                self.after(1000)
                if correct:
                    parent.update_score()
                else:
                    self.lives -= 1
                    parent.update_lives(self.lives)
                    if self.lives <= 0:
                        self.end_game(parent, main_app)
                        return
                self.init_round()
                

    def get_all_questions(self):
        with open("assets/words_list.txt", 'r', encoding = "utf8") as f: # utf8 encoding is used to handle some characters
            questions = [dict(zip(("question", "answer"), (line.strip().split(":")))) for line in f if ":" in line]
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

    def draw_border(self):
        # Animation for the border (Unused, will work on it if I have the time)
        return
        self.border = turtle.RawTurtle(self)
        #self.border.hideturtle()
        self.border.color("white")
        self.border.penup()
        self.border.pensize(3)
        self.border.forward(int(self.__getitem__("width")))
        self.border.right(90)
        self.border.forward(int(self.__getitem__("height")))
        self.border.right(90)
        self.border.forward(int(self.__getitem__("width")))
        self.border.right(90)
        self.border.forward(int(self.__getitem__("height")))

    def end_game(self, parent, main_app: MainApp):
        self.screen.resetscreen()

        # Turtle dying animation
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
        self.after(500)
        self.t.forward(200)
        self.after(500)
        self.t.left(90)
        self.after(500)
        self.t.color("light grey")
        self.screen.delay(10) # Return delay to default value

        self.after(1000)
        ttk.Label(self, text = "You Died!", background = "black", foreground = "white", justify = "center", 
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
                                command = lambda: main_app.goto_page(GamePage))
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
    def __init__(self, parent, main_app: MainApp, canvas_type = GameCanvas):
        super().__init__(parent, relief = "solid",borderwidth = 0) # Initialize GamePage as a child class of ttk.Frame
        self.window_size = (960,540)

        self.info_frame = ttk.Frame(self)
        self.info_frame.grid(column = 0, row = 0)
        self.score = 0
        self.scoreStr = tk.StringVar(self, "Score: {}".format(self.score))
        score_label = ttk.Label(self.info_frame, textvariable = self.scoreStr, justify = "center", font = ("TkDefaultFont", 30))
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
    def __init__(self, parent, main_app: MainApp):
        super().__init__(parent, main_app, canvas_type = InfiniteGameCanvas)
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