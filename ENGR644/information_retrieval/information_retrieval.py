#!/usr/bin/env python

'''
information_retrieval.py
'''

import string
import pandas as pd

def normalize_text(line):
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
                processed_line = normalize_text(line)
                dictionary[paragraph_count] = list(processed_line)
    return dictionary

def process_single_line(line_content):
    pass

def process_entire_doc(filename, read_bit):
    words_dict = {}
    doc_tracker = {}

    total_doc_dict = process_file(filename, read_bit)
    for doc_number, doc_content in total_doc_dict.iteritems():
        for word in doc_content:
            # Collection (Term) frequency logic
            # ========================================
            if word in words_dict.keys():
                words_dict[word][0] += 1
                # Document frequency logic
                # ========================================
                if doc_number != doc_tracker[word]:
                    words_dict[word][1] += 1
                    doc_tracker[word] = doc_number
            else:
                # For first pass, every word that currently exist in
                # doc_content is in at LEAST one document
                words_dict[word] = [1, 1]
                doc_tracker[word] = doc_number

        # Debugging output
        # if doc_number == 3:
        #     break
    return  words_dict

def process_file_once(filename, read_bit):
    paragraph_count = 0
    lexicon = {}

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
                normalized_line = normalize_text(line)
                lexicon[paragraph_count] = list(normaalized_line)
    return lexicon


def write_to_file(filename, data_dict):
    df = pd.DataFrame(data_dict)
    df.transpose().to_csv(filename, header=None)


def main():

    user_choice = int(raw_input("Select 1 for lesmis and 2 for bible (Exit = 3): "))

    if user_choice == 3:
        print "Exiting, goodbye"

    else:
        # Homework work 1
        # ========================================
        if user_choice == 0:
            print("Processing bible-sub\n")
            output_filename = 'bible-asv-sub-output.csv'
            data = process_entire_doc('bible-asv-sub.txt', 'r')
        elif user_choice == 1:
            print("Processing lesmis\n")
            output_filename = 'lesmis-output.csv'
            data = process_entire_doc('lesmis.txt', 'r')
        elif user_choice == 2:
            print("Processing bible\n")
            output_filename = 'bible-asv-output.csv'
            data =  process_entire_doc('bible-asv.txt', 'r')

        # Writing data to output file
        try:
            write_to_file(output_filename, data)
        except e:
            print("something went wrong")
        
if __name__ == "__main__":
    main()
