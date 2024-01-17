import os
from time import sleep

def check_for_stop_words(input_string, stop_words_list):
    return any(word in input_string for word in stop_words_list)
