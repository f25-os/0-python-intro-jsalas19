#! /bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2024/8/27
# @Author  : Joshua Salas
# @File    : OldWordCount.py

import os
import sys
import re

def word_count(file_path):
    if not os.path.isfile(file_path):   #check if file exists
        print(f"File not found: {file_path}")
        return

    with os.open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        words = [word.lower() for word in re.split(r'[\W_]+', text) if word]    #split by non-alphanumeric characters and convert to lowercase
        num_words = {}
        for word in words:
            word = word.lower()
            if word in num_words:
                num_words[word] = num_words.get(word, 0) + 1    #increment count if word exists
            else:
                num_words[word] = 1                      #initialize count if word does not exist
        
        sorted_words = sorted(num_words.items(), key=lambda x: x[0], reverse=False) #sort alphabetically
    
    with os.open('word_count.txt', 'w', encoding='utf-8') as output_file:
        for word, count in sorted_words:
            output_file.write(f"{word} {count}\n")  #write each word and its count to the file

    sys.stdout.write("Word count completed. Results saved to 'word_count.txt'.")
    

def compare_files(file1, file2):
    if not os.path.isfile(file1) or not os.path.isfile(file2):      #check if both files exist
        sys.stdout.write("One or both files to compare do not exist.")
        return
    
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        content1 = [line.strip() for line in f1.readlines()]        #strip() to remove \n at the end of each line
        content2 = [line.strip() for line in f2.readlines()]

    differences = [line for line in content1 if line not in content2]   #list comprehension to find differences
    
    if differences:
        print("Differences found:")
        for line in differences:            
            print(line)                 #print each differing line
    #else:
        #print("Perfect! No differences found.")

if __name__ == "__main__":
    if len(sys.argv) != 3:          #check for correct number of arguments
        print("Usage: python MyWordCount.py <input_file> [comparison_file] \n")
        sys.exit(1)
    input_file = sys.argv[1] 
    comparison_file = sys.argv[2]

    word_count(input_file)
    
    compare_files('word_count.txt', comparison_file) if comparison_file else None