#!/usr/bin/env python

'''
information_retrieval.py
'''

from __future__ import print_function
import string
import pandas as pd
import pickle

def normalize_text(line):
    '''
    normalize_text(line):

    Normalizes texts and returns a cleaned easily parsed version of the text.
    '''
    new_line = line.strip()         # Remove \n
    # Removing punctuation
    new_line = new_line.translate(None, string.punctuation)
    new_line = new_line.lower()     # Making lower case
    new_line = new_line.split()     # Remove extra spaces
    return new_line

def process_file(filename, read_bit):
    '''
    process_file(filename, read_bit):
    
    Processes a corpus to return
        {doc_id: [normalized list of terms in document], ...}
    '''
    paragraph_count = 0
    dictionary = {}

    with open(filename, read_bit) as file_pointer:
        for line in file_pointer:
            if "<P ID=" in line: # Open paragraph flag
                paragraph_count += 1
                continue
            elif "</P>" in line: # Close paragraph flag
                continue

            # If line is empty, do not process
            if line != "\n":
                processed_line = normalize_text(line)
                dictionary[paragraph_count] = list(processed_line)
    return dictionary

def process_entire_doc(filename):
    '''
    process_entire_doc(filename):

    Processes a Python dictionary of the form  
        {doc_id: [normalized list of terms in document], ...}
    to return a dictionary of
        {terms: [the term frequency, and document frequence], ...}
    '''
    words_dict = {}
    doc_tracker = {}

    total_doc_dict = process_file(filename, 'r')
    for doc_number, doc_content in total_doc_dict.iteritems():
        for word in doc_content:
            # Collection (Term) frequency logic
            if word in words_dict.keys():
                words_dict[word][0] += 1
                # Document frequency logic
                if doc_number != doc_tracker[word]:
                    words_dict[word][1] += 1
                    doc_tracker[word] = doc_number
            else:
                # For first pass, every word that currently exist in
                # doc_content is in at LEAST one document
                words_dict[word] = [1, 1]
                doc_tracker[word] = doc_number
    return  words_dict

def process_file_once(filename):
    '''
    process_file_once(filename):

    Combines the functions of process_file and process_entire_doc. Processes a
    corpus of terms and returns two dictionaries
        {term: [term freq, doc freq], ...} AND {(term, doc_id): doc freq, ...}
    Used to both create the dictionary (first returned dictionary) and to
    create the inverted file (second returned dictionary).
    '''
    doc_id = 0
    lexicon = {}
    doc_tracker = {}
    lexicon_inverted = {}

    with open(filename, 'r') as file_pointer:
        for line in file_pointer:
            if "<P ID=" in line: # Open paragraph flag
                doc_id += 1
                continue
            elif "</P>" in line: # Close paragraph flag
                continue

            # If line is empty, do not process
            if line != "\n":
                normalized_line = normalize_text(line)
                # Process the line of text the moment it is encountered.
                for term in list(normalized_line):
                    # Collection (Term) frequency logic
                    if term in lexicon.keys():
                        lexicon[term][0] += 1
                        # Document frequency logic
                        if doc_id != doc_tracker[term]:
                            lexicon[term][1] += 1
                            doc_tracker[term] = doc_id
                    else:
                        # For first pass, every term that currently exist in
                        # doc_content is in at LEAST one document
                        lexicon[term] = [1, 1]
                        doc_tracker[term] = doc_id

                    # Inverted File logic using tuple as key
                    if (term, doc_id) in lexicon_inverted.keys():
                        lexicon_inverted[term, doc_id] += 1
                    else:
                        lexicon_inverted[term, doc_id] = 1
        return lexicon, lexicon_inverted, test

def format_output_filename(input_filename, new_extension=None, append='output'):
    '''
    format_output_filename(input_filename, new_extension=None, append='output')

    Takes in an input_filename and returns an appropriate output_filename.
    Some customization is provided.
    '''
    common_extension = ['txt', 'json', 'csv', 'pickle']
    split_filename = input_filename.rsplit('.', 1)
    extension = split_filename[-1]

    if extension in common_extension:
        if new_extension is None or new_extension == extension:
            output_filename = split_filename[0] + "-" + append + "." + extension
        # elif new_extension 
        elif new_extension != extension:
            output_filename = split_filename[0]  + "." + new_extension
    return output_filename

def write_dict_to_file(filename, data_dict):
    '''
    write_dict_to_file(filename, data_dict):
    
    Writes a data dictionary to a CSV file with format: 
        TERM, TERM FREQ, DOC FREQ.
    '''
    df = pd.DataFrame(data_dict)
    df.transpose().to_csv(filename, header=None)


def main():

    user_choice = int(raw_input("Select 1 for lesmis and 2 for bible (Exit = 3): "))

    if user_choice == 3:
        print("Exiting, goodbye")
    else:
        if user_choice == 0:
            filename = 'bible-asv-sub.txt'
        elif user_choice == 1:
            filename = 'lesmis.txt'
        elif user_choice == 2:
            filename = 'bible-asv.txt'

        try:
            # Homework work 1
            # ========================================
            print("Processing", filename)
            # data = process_entire_doc(filename)
            data, inverted_data, test = process_file_once(filename)

            # print(inverted_data)
            # print(test)

            # with open('test.pickle', 'wb') as fp:
            #     pickle.dump(test, fp)

            output_filename = format_output_filename(filename, 'csv', 'dict')

            print("Writing term dictionary to ...", output_filename)
            write_dict_to_file(output_filename, data)

            # Homework 2
            # ========================================
            if inverted_data != None: # Process if inverted_data exist
                output_filename = format_output_filename(filename, 'pickle')

                print("Writing index to ...", output_filename)
                with open(output_filename, 'wb') as fp:
                    pickle.dump(inverted_data, fp)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
