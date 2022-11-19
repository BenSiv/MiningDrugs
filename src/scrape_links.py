"""
Scraping all links from a given website
"""

# import modules
import argparse
from bs4 import BeautifulSoup
from cmd_args import save_args, load_args
from scrape_page import get_soup_object

# argparse function
def get_args(argv=None):
    """
    Takes arguments from the user when running as a command line script
    """
    parser = argparse.ArgumentParser(description="Scraping all links from a given website")
    parser.add_argument("-w","--website", help="website to scrape", required=True)
    parser.add_argument("-o","--output_file", help="name of the file to save the output")
    parser.add_argument("-i", "--interactive", action="store_true", help="saves all the arguments to CmdArgs.yaml")
    parser.add_argument("-t", "--tests", action="store_true", help="runs tests for this script")
    return vars(parser.parse_args(argv))


def get_urls(base_url,soup):
    """Retrives all links from a BeautifulSoup object"""
    urls = [f"{base_url}{link.get('href')}" for link in soup.find_all('a')]
    return urls


def find_all(a_str, sub):
    """generator to gind all occurences in string"""
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)


def extract_base_url(url):
    """extracts base url to build full path later"""
    up_to = list(find_all(url, "/"))[2] # third '/' in the url
    return url[:up_to]


def scrape_links(website, output_file=None):
    """
    Wrapper function to call as module.function
    """
    
    base_url = extract_base_url(website)
    soup = get_soup_object(website)
    urls = get_urls(base_url, soup)
    unique_urls = list(set(urls))
    
    if output_file is not None:
        with open(output_file, "w") as output:
            output.write('\n'.join(unique_urls))
    else:
        return unique_urls

# tests

def main():
    """
    Runs the script through
    """
    args = get_args()

    if args["interactive"]:
        save_args(args)
    # args = load_args()

    if args["tests"]:
        # tests
        pass

    scrape_links(args["website"],args["output_file"])


if __name__ == "__main__":
    main()
