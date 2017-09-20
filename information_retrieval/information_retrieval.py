#!/usr/bin/env python

'''
information_retrieval.py

This

'''

import string

def process_line(line):
    # Remove \n
    line = line.strip()
    # Removing punctuation
    line = line.translate(None, string.punctuation)
    # Making lower case
    line = line.lower()
    return line.split()

def process_file(filename, read_bit):

    paragraph_count = 0
    dictionary = {}
    unique_word_per = 0

    with open(filename, read_bit) as file_pointer:
        for line in file_pointer:
            # Open paragraph flag
            if "<P ID=" in line:
                paragraph_count += 1
                continue
            # Close paragraph flag
            elif "</P>" in line:
                continue

            # If line is empty, do not process
            if line != "\n":
                processed_line = process_line(line)
                dictionary[paragraph_count] = list(processed_line)

    print dictionary
def main():

    '''     
    user_choice = int(raw_input("Select 1 for lesmis and 2 for bible: "))

    if user_choice == 1:
        process_file('bible-asv.txt', 'r')
    elif user_choice == 2:
        process_file('bible-asv.txt', 'r') 
    '''

    process_file('bible-asv-sub.txt', 'r')

if __name__ == "__main__":
    main()