import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    """
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    """

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    print(page, len(corpus[page]))
    
    model = {}
    links = corpus[page]

    # If page has no outgoing links, return a model (probability distribution) 
    # that chooses randomly among all pages with equal probability.
    if len(links) == 0:
        for key in corpus.keys():
            model[key] = 1 / len(corpus.keys())
        return model

    # Populate a model where a random surfer will randomicaly choose from 
    # current page links with damping_factor probability, and choose from 
    # all pages in corpus with (1 - damping_factor) probability.
    for link in links:
        model[link] = 1 / len(links) * damping_factor

    for key in corpus.keys():
        if key not in model.keys():
            model[key] = 1 / len(corpus) * (1 - damping_factor)
        else:
            model[key] += 1 / len(corpus) * (1 - damping_factor)

    return model

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError

    page = random.choice(list(corpus))
    model = transition_model(corpus, page, damping_factor)
    print(model)

    return {"1.html": .25, "2.html": .25, "3.html": .50}

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
