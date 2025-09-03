#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2024/9/3
# @Author  : Joshua Salas
# @File    : MyWordCount.py

import os
import sys
import re

BUFFER_SIZE = 4096  # bytes to read at a time

# Function to read entire file content
# @Param path: file path to read
# @Return: content of the file as a string
def read_file(path):
    fd = os.open(path, os.O_RDONLY)  # open file for reading
    chunks = []
    while True:
        data = os.read(fd, BUFFER_SIZE) # read a chunk
        if not data:
            break
        chunks.append(data.decode("utf-8", errors="ignore")) # decode bytes to string
    os.close(fd)                                            
    return "".join(chunks)  # join all chunks into a single string

# Function to write text to a file
# @Param path: file path to write
# @Param text: text content to write
# @Return: None
def write_file(path, text):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)  # open file for writing (create if doesnt exist, truncate if exists)
    os.write(fd, text.encode("utf-8"))
    os.close(fd)

# Function to compare two files for equality
# @Param file1: path to first file
# @Param file2: path to second file
# @Return: True if files are identical, False otherwise
def compare_files(file1, file2):
    fd1 = os.open(file1, os.O_RDONLY)
    fd2 = os.open(file2, os.O_RDONLY)

    try:
        while True:
            chunk1 = os.read(fd1, BUFFER_SIZE)
            chunk2 = os.read(fd2, BUFFER_SIZE)

            if chunk1 != chunk2:
                return False  # mismatch found

            if not chunk1 and not chunk2:
                return True  # both ended, no mismatch
    finally:
        os.close(fd1)
        os.close(fd2)

# Main function to execute word count and comparison
# Usage: python MyWordCount.py input.txt output_key.txt
def main():
    if len(sys.argv) != 3:
        sys.stdout.write(f"Usage: {sys.argv[0]} input.txt output_key.txt")
        sys.exit(1)

    input_file, comparison_file = sys.argv[1], sys.argv[2]

    # 1. Read file
    content = read_file(input_file)

    # 2. Extract words (case-insensitive, ignore punctuation/whitespace, lowercase-only)
    words = re.findall(r"[a-zA-Z0-9]+", content.lower())

    # 3. Count words
    num_words = {}
    for word in words:
        num_words[word] = num_words.get(word, 0) + 1

    # 4. Sort alphabetically
    sorted_counts = sorted(num_words.items(), key=lambda x: x[0], reverse=False)

    # 5. Format output
    output_lines = [f"{word} {count}" for word, count in sorted_counts]
    output_text = "\n".join(output_lines) + "\n"

    # 6. Write output
    write_file("word_count.txt", output_text)

    # 7. Compare files (Just to ensure correctness)
    if compare_files("word_count.txt", comparison_file):
        sys.stdout.write("Perfect! No differences found.\n")
    else:
        sys.stdout.write("Differences found.\n")

main()

