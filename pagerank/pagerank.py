import copy
import math
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

    # If the page has no links, there is an equal probability for each page in the corpus
    if not corpus[page]:
        equal_probability_for_each_page = 1 / len(corpus)
        return {p: equal_probability_for_each_page for p in corpus}

    # Based on the dampening factor, every page has a base probability
    base_random_probability = (1 - damping_factor) / len(corpus)
    res = {p: base_random_probability for p in corpus}

    # All linked pages have an equal chance of appearing
    linked_pages = corpus[page]
    linked_pages_probability = damping_factor / len(linked_pages)
    for linked_page in linked_pages:
        res[linked_page] += linked_pages_probability

    return res


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    res = {page: 0.0 for page in corpus}
    pages = list(corpus.keys())
    page = random.choice(pages)

    for i in range(n):
        tm = transition_model(corpus, page, damping_factor)
        probabilities = tm.values()

        page = random.choices(pages, weights=list(probabilities))[0]
        res[page] += (1 / n)

    return res


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    res = {p: 1 / total_pages for p in corpus}

    diff = math.inf
    min_diff = 0.001
    base_probability = (1 - damping_factor) / total_pages

    while diff > min_diff:
        old = copy.deepcopy(res)
        for page in corpus:
            res[page] = base_probability + sum_of_linking_pages(corpus, page, res, damping_factor)
            diff = abs(old[page] - res[page])
    return res


def sum_of_linking_pages(corpus, page, distributions, damping_factor):
    total = 0.0
    for p in corpus:
        if page in corpus[p]:
            total += distributions[p] / len(corpus[p])
    return damping_factor * total


if __name__ == "__main__":
    main()
