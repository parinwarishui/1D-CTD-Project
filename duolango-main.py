import tkinter as tk
from tkinter import ttk
import random
import turtle
import time
import copy
from copy import deepcopy
import time

# set number of variables in the game
lives = 3  #no. of times one can answer wrongly before game over
TOTAL_QUESTIONS = 10 # total questions per game
correct_answer = None
selected_answer = None
score = 0
questions_asked = 0

# dictionary contains all words -- for testing version -- qns, ans
words_list = [
    {"word": "Selamat", "translation": "Congratulations"},
    {"word": "Rumah", "translation": "House"},
    {"word": "Mimpi", "translation": "Dream"},
    {"word": "Buku", "translation": "Book"},
    {"word": "Kebun", "translation": "Garden"},
    {"word": "Pantai", "translation": "Beach"},
    {"word": "Kopi", "translation": "Coffee"},
    {"word": "Pohon", "translation": "Tree"},
    {"word": "Lagu", "translation": "Song"},
    {"word": "Gunung", "translation": "Mountain"},

    {"word": "你好 (Nǐ hǎo)", "translation": "Hello"},
    {"word": "家 (Jiā)", "translation": "Home"},
    {"word": "孩子 (Háizi)", "translation": "Child"},
    {"word": "学习 (Xuéxí)", "translation": "Study"},
    {"word": "星星 (Xīngxīng)", "translation": "Star"},
    {"word": "花 (Huā)", "translation": "Flower"},
    {"word": "音乐 (Yīnyuè)", "translation": "Music"},
    {"word": "工作 (Gōngzuò)", "translation": "Work"},
    {"word": "河 (Hé)", "translation": "River"},
    {"word": "果实 (Guǒshí)", "translation": "Fruit"},

    {"word": "नमस्ते (Namaste)", "translation": "Greetings"},
    {"word": "पर्वत (Parvat)", "translation": "Mountain"},
    {"word": "सपना (Sapna)", "translation": "Dream"},
    {"word": "चाँदनी (Chaandni)", "translation": "Moonlight"},
    {"word": "तारा (Tara)", "translation": "Star"},
    {"word": "संगीत (Sangeet)", "translation": "Music"},
    {"word": "पक्षी (Pakshi)", "translation": "Bird"},
    {"word": "नदी (Nadi)", "translation": "River"},
    {"word": "आकाश (Aakash)", "translation": "Sky"},
    {"word": "खेत (Khet)", "translation": "Field"},

    {"word": "สวัสดีครับ (Sawasdee Khrab)", "translation": "Welcome"},
    {"word": "ภูเขาไฟ (Phu Khao Fai)", "translation": "Volcano"},
    {"word": "ดวงจันทร์ (Duang Chan)", "translation": "Moon"},
    {"word": "ดอกไม้ (Dok Mai)", "translation": "Flower"},
    {"word": "ทะเล (Thale)", "translation": "Sea"},
    {"word": "นก (Nok)", "translation": "Bird"},
    {"word": "ฟ้า (Fah)", "translation": "Sky"},
    {"word": "เพลง (Phleng)", "translation": "Song"},
    {"word": "หมู่บ้าน (Moo Ban)", "translation": "Village"},
    {"word": "สวน (Suan)", "translation": "Garden"},

    {"word": "Makanan", "translation": "Food"},
    {"word": "爱 (Ài)", "translation": "Love"},
    {"word": "灯 (Dēng)", "translation": "Lamp"},
    {"word": "शांति (Shanti)", "translation": "Peace"},
    {"word": "ผีเสื้อ (Phee Suea)", "translation": "Butterfly"},
    {"word": "Bayangan", "translation": "Shadow"},
    {"word": "Gula", "translation": "Sugar"},
    {"word": "书包 (Shūbāo)", "translation": "Schoolbag"},
    {"word": "चाय (Chai)", "translation": "Tea"},
    {"word": "เรือ (Ruea)", "translation": "Boat"}]

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


#score_board display
scoreboard = turtle.Turtle()
scoreboard.hideturtle()
scoreboard.penup()
scoreboard.color("white")
scoreboard.goto(150, 270)

#game over display
game_over_board = turtle.Turtle()
game_over_board.hideturtle()
game_over_board.penup()
game_over_board.color("white")
game_over_board.goto(10, 70)

# Lives display
lives_display = turtle.Turtle()
lives_display.hideturtle()
lives_display.penup()
lives_display.color("red")
lives_display.goto(-250, 270)  # Position on top-left corner

def load_question():
    global current_words_list
    global current_question
    global all_answers
    global wrong_answers

    #check if its game over
    if questions_asked == TOTAL_QUESTIONS:
        end_game("Game Over! You've completed all questions!")
        return

    # randomly select one item, and "pop" that exact item out by index
    current_question = current_words_list.pop(current_words_list.index(random.choice(current_words_list)))

    # format the string for the question, sub in the current question word
    question_string = "What does {0} mean?".format(current_question["word"])

    question_display.clear()
    question_display.write(question_string, align="center", font=("Arial", 12, "bold"))

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

def update_scoreboard():
    """updating score """
    scoreboard.clear()
    scoreboard.write(
        f"Score: {score} | Questions: {questions_asked}/{TOTAL_QUESTIONS}",
        align="center",
        font=("Arial", 14, "normal")
    )
# Update lives on the screen
def update_lives():
    lives_display.clear()
    hearts = "❤️" * lives
    lives_display.write(f"Lives: {hearts}", align="left", font=("Arial", 16, "bold"))


def check_collision():
    global score, lives, questions_asked

    for textbox in answers:
        if player.distance(textbox) < 50:  # Collision detected
            answer = answer_text_map[textbox]  # Get the answer variable

            if answer == current_question["translation"]:
                print("Correct! The answer was:", current_question["translation"])
                score += 1
            else:
                print("Wrong! The answer was:", current_question["translation"])
                lives -= 1

            questions_asked += 1

            # Check for game-over conditions
            if questions_asked == TOTAL_QUESTIONS:
                end_game("Game Over! You've completed all questions!")
                return
            elif lives == 0:
                end_game("Game Over! You lost all your lives!")
                return

            # Reset player and load the next question
            player.goto(0, 0)
            load_question()
            update_scoreboard()
            update_lives()
            break

def end_game(message):
    """End the game and display a message."""
    player.hideturtle()
    question_display.clear()
    scoreboard.clear()
    lives_display.clear()

    # Display the game over message
    game_over_board.write(
        message,
        align="center",
        font=("Arial", 15, "bold"),

    )

    # Stop movement
    screen.onkeypress(None, "w")
    screen.onkeypress(None, "a")
    screen.onkeypress(None, "s")
    screen.onkeypress(None, "d")

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

# Initialize the first question and display
load_question()
update_scoreboard()
update_lives()

# Start the game loop

game_loop()
screen.mainloop()

# use screen.listen() and screen.onkeypress() to allow functions using our keyboard input

# function to reset the window, possible conditions are:
## go to next question

# open random question in TOTAL_QUESTIONS
## go to "you won!" window after last question
# you_won_video()


## go to "you lost!" window after losing all lives
# lives == 0
# def you_lost():
#    if TOTAL_HEARTS == 0:
#        print("you lost!")s
# you_lost()


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
# print(options)


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
# turtle_elements = #answer of the question
## config to display the question (along with everything else)

# SAVE FOR LATER
# function to check if turtle has "touched" the answers
# turtle.value() == answer_cooordinates
## if touched any of the answers
# if turtle.value() == answer_cooordinates:
#    generate question

### check if correct or not -> then update question, points, lives, etc
## if times up before touching
### -1 lives -> update question
# random.TOTAL_QUESTIONS:

'''
question_label = tk.Label(root, text="", font=("Arial", 16))
question_label.pack()

root.mainloop()
'''

'''
===========================================================
'''