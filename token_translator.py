#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is a script that takes token from one tier and writes translations
    of each token to another tier. The translation is done with a dictionary
    in CSV format.

History:
-- V0.1: basic script architecture, tokenizes itself, prints translations in 
         stdout, filepaths hardcoded

"""

import glob     # Import glob to easily loop over files
import pympi    # Import pympi to work with elan files
import string   # Import string to get the punctuation data
import csv      # Import csv to handle dictionary data

# Define some variables for later use
corpus_root = './examples_pympi'
input_file = '{}/Test_muyu_001.eaf'.format(corpus_root)
output_file = '{}/Test_muyu_001_glossed.eaf'.format(corpus_root)
ort_tier_names = ['tx']
dict_file = '{}/Test_dict.txt'.format(corpus_root)
dict_data = {}

# Initialize the elan file
eafob = pympi.Elan.Eaf(input_file)

# read the dictionary from file
with open(dict_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        dict_data[row[0]] = row[1]
        
# Loop over all the defined tiers that contain orthography
for ort_tier in ort_tier_names:
    # If the tier is not present in the elan file spew an error and
    # continue. This is done to avoid possible KeyErrors
    if ort_tier not in eafob.get_tier_names():
        print 'WARNING!!!'
        print 'One of the ortography tiers is not present in the elan file'
        print 'namely: {}. skipping this one...'.format(ort_tier)
    # If the tier is present we can loop through the annotation data
    else:
        for annotation in eafob.get_annotation_data_for_tier(ort_tier):
            # We are only interested in the utterance
            utterance = annotation[2]
            # Split, by default, splits on whitespace thus separating words
            words = utterance.split()
            # For every word ...
            for word in words:
                # Remove the possible punctuation
                for char in string.punctuation:
                     word = word.replace(char, '')
                # Convert to lowercase
                word = word.lower()
                # now translate it if possible
                tw = dict_data.get(word)
                if tw is not None:
                    print '{} - {}'.format(word, tw)

