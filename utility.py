import sys
import termios
import tty
import time

clear_screen = "\x1b[2J\x1b[H"
color_black = "\u001b[30m"
color_red = "\u001b[31m"
color_green = "\u001b[32m"
color_yellow = "\u001b[33m"
color_blue = "\u001b[34m"
color_magenta = "\u001b[35m"
color_cyan = "\u001b[36m"
color_white = "\u001b[37m"
color_reset = "\u001b[0m"

color_bkgnd_yellow = "\u001b[43;1m"
color_bkgnd_black = "\u001b[40;1m"


class Webpage:
    def __init__(self, url, words, links):
        self.url = url
        self.words = words
        self.links = links
        self.num_words = len(words)
        self.num_links = 0
        self.weight = 1.0           # initial weight; used later for Pagerank

def read_raw_pages(file):
    with open(file, 'r') as f:
        # Read all lines and remove newline characters
        lines = [line.strip() for line in f]
    raw_pages = []
    i = 0
    while i < len(lines):
        # Each page is represented by 3 consecutive lines
        if i + 2 >= len(lines):
            break
        url_line = lines[i]
        content_line = lines[i+1]
        links_line = lines[i+2]
        i += 3

        # Extract URL from "URL:" line
        if url_line.startswith("URL:"):
            url = url_line[4:].strip()
        else:
            continue  # skip if no URL

        # Extract words from "CONTENT:" line
        words = []
        if content_line.startswith("CONTENT:"):
            content = content_line[8:].strip()
            if content:
                words = content.split()
        
        # Extract links from "LINKS:" line
        links = []
        if links_line.startswith("LINKS:"):
            links_str = links_line[6:].strip()
            if links_str:
                links = links_str.split()
        
        raw_pages.append({
            'url': url,
            'words': words,
            'links': links
        })
    return raw_pages

def build_pages(raw_pages):
    pages = []
    url_to_index = {}
    # Build URL-to-index mapping and initialize Webpage objects
    for index, page_data in enumerate(raw_pages):
        url_to_index[page_data['url']] = index
        pages.append(Webpage(page_data['url'], page_data['words'], page_data['links']))
    return pages, url_to_index

def process_links(pages, url_to_index):
    for page in pages:
        valid_link_indices = []
        for link in page.links:
            # Only include links that refer to an internal page
            if link in url_to_index:
                valid_link_indices.append(url_to_index[link])
        page.links = valid_link_indices
        page.num_links = len(valid_link_indices)

def read_input_file(file):
    raw_pages = read_raw_pages(file)
    pages, url_to_index = build_pages(raw_pages)
    process_links(pages, url_to_index)
    return pages

# Global variable: load pages at program startup.
pages = read_input_file("sample-domain.txt")


class IndexWord:
    def __init__(self, text):
        self.text = text
        self.pages = []
        self.num_pages = 0

def build_word_index(pages):
    index = {}
    for i, page in enumerate(pages):
        # Use a set to ensure each page is added only once per unique word
        unique_words = set(page.words)
        for word in unique_words:
            # Convert word to lowercase
            w = word.lower()
            if w not in index:
                index[w] = IndexWord(w)
            index[w].pages.append(i)
    # Set the num_pages field for each indexed word
    for w in index:
        index[w].num_pages = len(index[w].pages)
    return index

# Build the global word index after loading pages.
if pages:
    word_index = build_word_index(pages)
else:
    word_index = {}

def generate_snippet(page, query, context=5):
    """
    Generate a snippet from page.words where the query first occurs,
    including a few words before and after the query.
    The searched word is highlighted using color_yellow.
    """
    words = page.words
    try:
        # Find the first occurrence of the query word
        i = next(i for i, w in enumerate(words) if w.lower() == query)
    except StopIteration:
        return "Snippet not available"
    start = max(0, i - context)
    end = min(len(words), i + context + 1)
    snippet_words = []
    for w in words[start:end]:
        if w.lower() == query:
            snippet_words.append(color_yellow + w + color_reset)
        else:
            snippet_words.append(w)
    snippet = " ".join(snippet_words)
    return snippet


def compute_pagerank(iterations=50):
    """
    Compute Pagerank by iterating 50 times. In each iteration:
    - Start by setting new weight for each page to 0.1
    - For each page, if it has outgoing links, distribute 90% of its weight equally among them.
      Otherwise, retain 90% of its weight.
    - Update the page weights with the new values.
    """
    N = len(pages)
    for _ in range(iterations):
        new_weights = [0.1] * N  # initialize new weight for each page 
        for i, page in enumerate(pages):
            if page.num_links > 0:
                distributed_weight = 0.9 * page.weight / page.num_links
                for j in page.links:
                    new_weights[j] += distributed_weight
            else:
                # If no outgoing links, the page keeps its 90% weight.
                new_weights[i] += 0.9 * page.weight
        # Update each page's weight
        for i in range(N):
            pages[i].weight = new_weights[i]

# Compute Pagerank on startup if pages exist.
if pages:
    compute_pagerank()

def predict(query):
    # If no query, display a simple summary.
    if query == "":
        output = color_cyan + f"{len(pages)} pages loaded\n" + color_reset
        sys.stdout.write(output)
        return

    # Convert query to lowercase for matching
    lowerq = query.lower()
    if lowerq in word_index:
        index_word = word_index[lowerq]
        total = index_word.num_pages

        # Sort matching pages in descending order by weight
        sorted_page_ids = sorted(index_word.pages, key=lambda pid: pages[pid].weight, reverse=True)

        # Print total matching pages (with color)
        output = color_cyan + f"{total} pages match\n\n" + color_reset

        # Print the top 5 results, numbered and with colors
        count = 1
        for page_id in sorted_page_ids[:5]:
            page = pages[page_id]
            snippet = generate_snippet(page, lowerq, context=5)
            output += color_blue + f"{count}. " + color_reset
            output += color_green + f"[{page.weight:.3f}] " + color_reset
            output += color_magenta + f"{page.url}\n" + color_reset
            output += color_white + f"   {snippet}\n\n" + color_reset
            count += 1
    else:
        output = color_red + f"No pages found for '{lowerq}'\n" + color_reset
    sys.stdout.write(output)

def process_keystrokes():
    query = ''
    ch = ' '
    fd = sys.stdin.fileno()
    while ch[0] != '\n' and ch[0] != '\r':
        sys.stdout.write(clear_screen)
        sys.stdout.write(color_green + "Search keyword: ")
        sys.stdout.write(color_white + query + color_green + "-\n\n")
        predict(query)
        sys.stdout.write(color_reset)
        sys.stdout.flush()
        
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        time.sleep(0.1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        sys.stdin.flush()

        if ord(ch[0]) == 8 or ord(ch[0]) == 127:  # backspace
            if len(query) > 0:
                query = query[:-1]
        elif ch[0] != '\n':
            query = query + ch

if __name__ == "__main__":
    process_keystrokes()
