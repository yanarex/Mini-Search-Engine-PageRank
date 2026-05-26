# Mini Search Engine with PageRank

A Python-based mini search engine that indexes webpage content, ranks search results using PageRank, and displays keyword matches with highlighted text snippets.

---

## Project Overview

This project implements a small search engine in Python. It reads a collection of webpage data, builds an index of searchable words, calculates page importance using a PageRank-style algorithm, and allows users to search for keywords interactively in the terminal.

The project was completed as a homework assignment and focuses on indexing, graph-based ranking, text processing, and search result presentation.

---

## Features

- Reads webpage data from a structured text file
- Stores each webpage's URL, content words, and outgoing links
- Builds an inverted index for keyword searching
- Calculates page rankings using a PageRank-style algorithm
- Sorts search results by page weight
- Displays the top matching pages
- Generates short snippets around the searched keyword
- Highlights the searched keyword in the terminal
- Supports interactive search input

---

## Future Improvements

- Add support for multi-word search queries
- Add better text cleaning and punctuation handling
- Add ranking based on both PageRank and word frequency
- Add a graphical or web-based interface
- Improve support for very large datasets
- Add unit tests for indexing and ranking functions
- Allow the input filename to be passed as a command-line argument

---

## Technologies Used

- Python 3
- File I/O
- Text Processing
- Inverted Indexing
- PageRank
- Graph Traversal Concepts
- Terminal ANSI Color Formatting

---

## Files

| File | Description |
|---|---|
| `utility.py` | Main program containing the search engine, index builder, PageRank calculation, and terminal interface |
| `asu-domain.txt` | Webpage dataset containing URLs, page content, and links |
| `README.md` | Project documentation |
| `.gitignore` | Files and folders ignored by Git |

---

## Dataset Format

The input file stores webpages in groups of three lines:

```text
URL: https://example.com
CONTENT: example page content words go here
LINKS: https://example.com/about https://example.com/contact