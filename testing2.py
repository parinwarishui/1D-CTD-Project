import tkinter
import turtle
import random
from copy import deepcopy

words_list = [
    {"word":"W1", "translation":"T1"},
    {"word":"W2", "translation":"T2"},
    {"word":"W3", "translation":"W3"},



    {"word":"W4", "translation":"T4"},
    {"word":"W5", "translation":"T5"},
    {"word":"W6", "translation":"W6"},
    {"word":"W7", "translation":"T7"},
    {"word":"W8", "translation":"T8"},
    {"word":"W9", "translation":"T9"},
    {"word":"W10", "translation":"T10"}
]

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
    while count < 3:
        options.append(available_choices.pop(random.randrange(0, len(available_choices)))) # Choose 1 random dict from list
        count += 1
    return options

print("OLD LIST BEFORE CHANGES", len(available_questions))
correct_pair = generate_new_question(available_questions)
print(correct_pair)
options = get_choices(words_list, correct_pair)
print(options)
print("NEW LIST AFTER CHANGES", len(available_questions))

current_question = correct_pair["word"]
answer_list = list(correct_pair["translation"])
print(answer_list)

'''

def ask_player(question_dict, answer_list): #input a list
    qn = question_dict["word"]
    ans = 
    randomized_order_ans =
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