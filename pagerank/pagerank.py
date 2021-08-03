import os
import random
import re
import sys
import copy

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
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


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
    pagerank = {}

    # Choose a random page to be the starting page
    page = random.choice(list(corpus))
    
    # Loop to generate n sample pages and 
    for i in range(n):
        model = transition_model(corpus, page, damping_factor)
        next_page = random.choices(list(model.keys()), weights=list(model.values()), k=1)[0]
        
        if next_page not in pagerank:
            pagerank[next_page] = 1
        else:
            pagerank[next_page] += 1

        page = next_page
    
    # Divide each page count by number of samples to obtain the probability
    for page in pagerank:
        pagerank[page] /= n 

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}

    # Set the initial pagerank of every page to 1 / N (equally likely to be on any page). 
    for page in corpus:
        pagerank[page] = 1 / len(corpus)
        
    has_converged = False
    while has_converged != True:
        current_pagerank = copy.deepcopy(pagerank)
        rank_difference = {}

        for page in corpus.keys():
            rank = 0
            # Find summation of PR(i) / NumLinks(i) for each page
            for page_i, links in corpus.items():
                if page in links:
                    rank += current_pagerank[page_i] / len(links)
                
                if len(links) == 0:
                    rank += 1 / len(corpus)

            # 
            pagerank[page] = ((1 - damping_factor) / len(corpus)) + (damping_factor * rank)
            
            rank_difference[page] = abs(current_pagerank[page] - pagerank[page])
            
        for page in rank_difference:
            if rank_difference[page] <= 0.001:
                has_converged = True

    # Normalize ranks (divide each rank by total rank) to guarantee that 
    # they sum up to 1 in case they already are not (i.e: corpus2).     
    total_rank = 0    
    for rank in pagerank.values():
        total_rank += rank

    for page in pagerank:
        pagerank[page] = pagerank[page] / total_rank

    return pagerank


if __name__ == "__main__":
    main()
