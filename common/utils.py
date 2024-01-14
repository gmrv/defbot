import os
from time import sleep

def message_has_links(input_string):
    return '@' in input_string or 't.me/' in input_string
