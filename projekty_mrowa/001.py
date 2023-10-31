# BEGIN: 7f6d5a7b6d9a
import argparse
from collections import Counter
from ascii_graph import Pyasciigraph
from ascii_graph import colors
import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable

parser = argparse.ArgumentParser(description="Book histogram generator")
parser.add_argument("filename", help="the name of the file to process")
parser.add_argument('--words', '-w', help="the number of words to plot", type=int, default=10)
parser.add_argument('--min_word_length', '-m', help="the minimum length of the word to plot", type=int, default=0)

args = parser.parse_args()

with open(args.filename, 'r', encoding='utf-8') as file:
    text = file.read()

# Split the text into words
words = text.split()

# Count the occurrences of each word
word_counts = Counter(words)

# Get the most common words
most_common_words = word_counts.most_common(args.words)

# Create a list of tuples for Pyasciigraph
data = [(word, count) for word, count in most_common_words]

# Create the graph
graph = Pyasciigraph()
for line in graph.graph('Word Frequency Histogram', data):
    print(line)

