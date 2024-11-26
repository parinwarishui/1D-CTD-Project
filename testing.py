from copy import deepcopy
import random

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
    {"word":"W10", "translation":"T10"},
    
]

available_questions = deepcopy(words_list)
def generate_new_question(available_questions):
    correct_pair = available_questions.pop(random.randrange(0, len(available_questions)))
    return correct_pair


def get_choices(words_list: list, correct_pair: dict):
    count = 0
    available_choices = deepcopy(words_list)
    available_choices.remove(correct_pair)
    options = []
    while count <= 5:
        options.append(available_choices.pop(random.randrange(0, len(available_choices)))) # Choose 1 random dict from list
        count += 1
    return options

question = generate_new_question(available_questions)
options = get_choices(words_list, question)
print(question)
print(options)