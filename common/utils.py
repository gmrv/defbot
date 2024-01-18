import os
import re
from time import sleep

def is_contains_stop_words(input_string, stop_words_list):
    return any(word in str.lower(input_string) for word in stop_words_list)

def contain_alphanumeric(word):
    if len(word) < 5: return False
    return any(char.isalpha() for char in word) and any(char.isdigit() for char in word)

def has_alphanumeric_words(text):
    words = re.findall(r'\b\w+\b', text)
    return any(contain_alphanumeric(word) for word in words)

def read_list_from_file(filename):
    # Initialize an empty list to store data from the file
    data_list = []

    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            # Read each line in the file
            for line in file:
                # Strip any leading or trailing whitespaces and add the line to the list
                if len(line.strip()) > 0:
                    data_list.append(line.strip())
    except FileNotFoundError:
        # Handle file not found exception
        print(f"File '{filename}' not found.")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

    # Return the list containing data from the file
    return data_list

def append_list_to_file(filename, words):
    try:
        # Open the file in append mode
        with open(filename, 'a') as file:
            # Iterate through the list of words and write each word to the file
            for word in words:
                file.write(str(word) + '\n')
        print(f"Successfully appended the list to '{filename}'.")
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")

def write_list_to_file(filename, list):
    try:
        # Open the file in write mode and write the elements from the result list
        with open(filename, 'w') as file:
            for item in list:
                file.write(str(item) + '\n')
        print(f"Successfully wrote the result to '{filename}'.")
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")

def remove_elements(list1, list2):
    # Use a list comprehension to create a new list without common elements
    result_list = [item for item in list1 if item not in list2]
    return result_list