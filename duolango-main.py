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
import copy
from copy import deepcopy

# set number of variables in the game
TOTAL_HEARTS = 3
TOTAL_QUESTIONS = 10
correct_answer = None
selected_answer = None

# dictionary contains all words -- for testing version -- qns, ans
words_list = [
    {"word": "W1", "translation": "T1"},
    {"word": "W2", "translation": "T2"},
    {"word": "W3", "translation": "W3"},
    {"word": "W4", "translation": "T4"},
    {"word": "W5", "translation": "T5"},
    {"word": "W6", "translation": "W6"},
    {"word": "W7", "translation": "T7"},
    {"word": "W8", "translation": "T8"},
    {"word": "W9", "translation": "T9"},
    {"word": "W10", "translation": "T10"},
    {"word": "W11", "translation": "T11"},
    {"word": "W12", "translation": "T12"},
    {"word": "W13", "translation": "T13"},
    {"word": "W14", "translation": "T14"},
    {"word": "W15", "translation": "T15"},
    {"word": "W16", "translation": "T16"},
    {"word": "W17", "translation": "T17"},
    {"word": "W18", "translation": "T18"},
    {"word": "W19", "translation": "T19"},
    {"word": "W20", "translation": "T20"},
    {"word": "W21", "translation": "T21"},
    {"word": "W22", "translation": "T22"},
    {"word": "W23", "translation": "T23"},
    {"word": "W24", "translation": "T24"},
    {"word": "W25", "translation": "T25"},
    {"word": "W26", "translation": "T26"},
    {"word": "W27", "translation": "T27"},
    {"word": "W28", "translation": "T28"},
    {"word": "W29", "translation": "T29"},
    {"word": "W30", "translation": "T30"},
    {"word": "W31", "translation": "T31"},
    {"word": "W32", "translation": "T32"},
    {"word": "W33", "translation": "T33"},
    {"word": "W34", "translation": "T34"},
    {"word": "W35", "translation": "T35"},
    {"word": "W36", "translation": "T36"},
    {"word": "W37", "translation": "T37"},
    {"word": "W38", "translation": "T38"},
    {"word": "W39", "translation": "T39"},
    {"word": "W40", "translation": "T40"},
    {"word": "W41", "translation": "T41"},
    {"word": "W42", "translation": "T42"},
    {"word": "W43", "translation": "T43"},
    {"word": "W44", "translation": "T44"},
    {"word": "W45", "translation": "T45"},
    {"word": "W46", "translation": "T46"},
    {"word": "W47", "translation": "T47"},
    {"word": "W48", "translation": "T48"},
    {"word": "W49", "translation": "T49"},
    {"word": "W50", "translation": "T50"}
]


'''
===========================================================
'''

'''
# initialize tkinter window
class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

MainGame = TkinterApp()

root.title = "Duolango"
'''

# Initialize the screen
screen = turtle.Screen()
screen.title("Duolango")
screen.bgcolor("black")
screen.setup(width=600, height=600)

# Create the player-controlled turtle
player = turtle.Turtle()
player.shape("turtle")
player.color("lime")
player.penup()
player.speed(0)

# Create a border
border = turtle.Turtle()
border.hideturtle()
border.penup()
border.color("white")
border.pensize(3)
border.goto(-300, -300)
border.pendown()
for _ in range(4):  # Draw a square border
    border.forward(600)
    border.left(90)

# Create a turtle to display the question
question_display = turtle.Turtle()
question_display.hideturtle()
question_display.penup()
question_display.color("white")
question_display.goto(0, 250)

# Create textboxes for answers
answers = []
answer_text_map = {}  # Maps textboxes to their current answers
corner_positions = [(-250, 250), (250, 250), (-250, -250), (250, -250)]

# Current question
current_question = None

# current list with remaining words
current_words_list = copy.copy(words_list)

def load_question():
    global current_words_list
    global current_question
    global all_answers
    global wrong_answers

    # randomly select one item, and "pop" that exact item out by index
    current_question = current_words_list.pop(current_words_list.index(random.choice(current_words_list)))
    
    # format the string for the question, sub in the current question word
    question_string = "What does {0} mean?".format(current_question["word"])

    question_display.clear()
    question_display.write(question_string, align="center", font=("Arial", 16, "bold"))

    # create a list of all "choices" for the question
    all_answers = [current_question["translation"]]
    
    # Get the wrong choices at random from the dict, and then add to the list of answers: all_answers
    wrong_answers = random.sample(current_words_list, 3)

    for i in wrong_answers:
        all_answers.append(i["translation"])

    random.shuffle(all_answers)
    
    # Update textboxes with new answers
    for pos, answer, textbox in zip(corner_positions, all_answers, answers):
        textbox.clear()
        textbox.goto(pos)
        textbox.write(answer, align="center", font=("Arial", 12, "normal"))
        answer_text_map[textbox] = answer  # Map textbox to its answer

# Initialize textboxes at corners
for pos in corner_positions:
    textbox = turtle.Turtle()
    textbox.hideturtle()
    textbox.penup()
    textbox.color("white")
    answers.append(textbox)

# Key state variables
keys = {"w": False, "a": False, "s": False, "d": False}

# Define functions
def check_boundaries():
    """Keep the player within the screen bounds."""
    x, y = player.xcor(), player.ycor()
    if x > 290:
        player.setx(290)
    if x < -290:
        player.setx(-290)
    if y > 290:
        player.sety(290)
    if y < -290:
        player.sety(-290)

def check_collision():
    """Check for collisions with textboxes."""
    for textbox in answers:
        if player.distance(textbox) < 50:  # Collision detected
            answer = answer_text_map[textbox]  # get answer variable
            # generate text for 2 cases, either we get the correct answer or incorrect answer
            if answer == current_question["translation"]:
                print("Correct! The answer was:", current_question["translation"])
            else:
                print("Wrong! The answer was:", current_question["translation"])
            player.goto(0, 0)  # reset player position back to center
            load_question()  # load the next question!
            break

def move_player():
    """Move the player based on key state."""
    if keys["w"] and keys["a"]:  # Up-left
        player.setheading(135)
    elif keys["w"] and keys["d"]:  # Up-right
        player.setheading(45)
    elif keys["s"] and keys["a"]:  # Down-left
        player.setheading(225)
    elif keys["s"] and keys["d"]:  # Down-right
        player.setheading(315)
    elif keys["w"]:  # Up
        player.setheading(90)
    elif keys["s"]:  # Down
        player.setheading(270)
    elif keys["a"]:  # Left
        player.setheading(180)
    elif keys["d"]:  # Right
        player.setheading(0)
    else:
        return  # No movement if no key is pressed

    player.forward(10)  # Move forward in the current direction
    check_boundaries()
    check_collision()

# Key press handlers
def press_key(key):
    keys[key] = True
    move_player()  # Call movement when a key is pressed

def release_key(key):
    keys[key] = False

# Bind key events
screen.listen()
screen.onkeypress(lambda: press_key("w"), "w")
screen.onkeypress(lambda: press_key("a"), "a")
screen.onkeypress(lambda: press_key("s"), "s")
screen.onkeypress(lambda: press_key("d"), "d")

screen.onkeyrelease(lambda: release_key("w"), "w")
screen.onkeyrelease(lambda: release_key("a"), "a")
screen.onkeyrelease(lambda: release_key("s"), "s")
screen.onkeyrelease(lambda: release_key("d"), "d")

# Main game loop
def game_loop():
    move_player()  # Check for player movement
    screen.ontimer(game_loop, 100)  # Call game_loop again after 100ms

# Initialize the first question
load_question()

game_loop()  # Start the game loop
screen.mainloop()

# use screen.listen() and screen.onkeypress() to allow functions using our keyboard input

# function to reset the window, possible conditions are:
## go to next question 

#open random question in TOTAL_QUESTIONS
## go to "you won!" window after last question
#you_won_video()


## go to "you lost!" window after losing all lives
#lives == 0
#def you_lost():
#    if TOTAL_HEARTS == 0:
#        print("you lost!")  
#you_lost()
    
    
    



# function to come up with the question
'''
available_questions = deepcopy(words_list)
def generate_new_question(available_questions) -> dict:
    correct_pair = available_questions.pop(random.randrange(0, len(available_questions)))
    return correct_pair

## select random wrong choices -- make sure they don't repeat
def get_choices(words_list: list, correct_pair: dict) -> list:
    count = 0
    available_choices = deepcopy(words_list)
    available_choices.remove(correct_pair)
    options = []
    while count < 5:
        options.append(available_choices.pop(random.randrange(0, len(available_choices)))) # Choose 1 random dict from list
        print(options)
        count += 1
    return options
'''
#print(options)


## generate text and accept input for answer and check if correct or not
'''
def ask_player(question_dict, answer_list): #input a list
    qn = question_dict["word"]
    ans = input("answer:")
    randomized_order_ans()
    print(f"What does {qn} mean?")
    for i in ans:
        print(f"{i}")
    player_input = input("Type answer: ")
    if player_input == (answer_list dict):
        print(True)
    else:
        print(wrong)
    lives = lives - 1
'''

# SAVE FOR LATER
## place answers on screen as "turtle elements"
#turtle_elements = #answer of the question
## config to display the question (along with everything else)

# SAVE FOR LATER
# function to check if turtle has "touched" the answers
#turtle.value() == answer_cooordinates
## if touched any of the answers
#if turtle.value() == answer_cooordinates:
#    generate question 
    
### check if correct or not -> then update question, points, lives, etc
## if times up before touching
### -1 lives -> update question
#random.TOTAL_QUESTIONS:
 
'''
question_label = tk.Label(root, text="", font=("Arial", 16))
question_label.pack()

root.mainloop()
'''

'''
===========================================================
'''
