# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 16:05:45 2023

@author: Matt
"""

import csv
import os
import nltk
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

def get_book_ids_from_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_='link')
        book_ids = []
        #print(links)

        for link in links:
            href = link.get('href', '')
            #print(href)
            book_id = href.split('/')[-1]
            #print(book_id)
            if book_id.isdigit():
                book_ids.append(int(book_id))

        return book_ids

    return []

def download_gutenberg_books(book_ids, output_folder):
    for book_id in book_ids:
        url = f'http://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'
        response = requests.get(url)
        
        if response.status_code == 200:
            text = response.text
            output_file_path = os.path.join(output_folder, f"{book_id}.txt")
            
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(text)

def extract_books_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sentences = nltk.sent_tokenize(file.read())

    # Keywords to look for in sentences
    keywords = ['device', 'machine', 'invention', 'contraption']

    # Placeholder for books descriptions and page numbers
    books_data = []

    # Add logic to identify and extract books descriptions
    for i, sentence in enumerate(sentences, start=1):

        if any(keyword in sentence.lower() for keyword in keywords):
            # Extract the previous and next sentences
            prev_sentence = sentences[i - 2] if i >= 2 else ""
            next_sentence = sentences[i] if i < len(sentences) else ""

            # Combine the sentences and add to device_data
            combined_sentences = f"{prev_sentence} {sentence} {next_sentence}".strip()
            books_data.append({'Page': i, 'Description': combined_sentences})

    return books_data

def save_to_csv(books_data, csv_file_path, book_title):
    # Check if the CSV file already exists
    file_exists = os.path.exists(csv_file_path)

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Book', 'Page', 'Description']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file is newly created
        if not file_exists:
            csv_writer.writeheader()

        # Write data to CSV file
        for data in books_data:
            data['Book'] = book_title
            csv_writer.writerow(data)

# Required URLs
gutenberg_url = r'https://www.gutenberg.org/ebooks/subject/36'
output_folder = r'C:\Users\Matt\Desktop\DH\output'
output_csv_path = r'C:\Users\Matt\Desktop\DH\output\output1.csv'

# Get book IDs from the specified URL
book_ids = get_book_ids_from_url(gutenberg_url)

# Download books and process them
for book_id in book_ids:
    download_gutenberg_books([book_id], output_folder)
    book_title = f"Gutenberg_{book_id}"
    book_file_path = os.path.join(output_folder, f"{book_id}.txt")
    books_data = extract_books_sentences(book_file_path)

    # Save the extracted device descriptions with page numbers to the CSV file
    save_to_csv(books_data, output_csv_path, book_title)

print(f"Books sentences with enumeration saved to {output_csv_path}")