import os
import re
from time import sleep

def is_contains_stop_words(input_string, stop_words_list):
    return any(word in input_string for word in stop_words_list)

def contain_alphanumeric(word):
    if len(word) < 5: return False
    return any(char.isalpha() for char in word) and any(char.isdigit() for char in word)

def has_alphanumeric_words(text):
    words = re.findall(r'\b\w+\b', text)
    return any(contain_alphanumeric(word) for word in words)

