"""
Scraping all links from a given website
"""

# import modules
import argparse
import toml
import requests
from bs4 import BeautifulSoup

# argparse function
def get_args(argv=None):
    """
    Takes arguments from the user when running as a command line script
    """
    parser = argparse.ArgumentParser(description="Scraping all links from a given website")
    parser.add_argument("-w","--website", help="website to scrape", required=True)
    parser.add_argument("-o","--output_file", help="name of the file to save the output")
    parser.add_argument("-i", "--interactive", action="store_true", help="saves all the arguments to CmdArgs.yaml")
    return vars(parser.parse_args(argv))


def save_args(args):
    """Saves command line arguments to CmdArgs.toml"""
    with open("CmdArgs.toml", "w") as toml_file:
        toml.dump(args, toml_file)


def load_args():
    """Loads command line arguments from CmdArgs.toml"""
    with open("CmdArgs.toml") as toml_file:
        args = toml.load(toml_file)
    for key,value in args.items():
        print(key, "=>", value)
    return args


def get_soup_object(URL):
    """
    Send a request to a page and return the response as a BeautifulSoup object
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content , 'html.parser')
    return soup


def get_urls(base_url,soup):
    """Retrives all links from a BeautifulSoup object"""
    urls = [f"{base_url}{link.get('href')}" for link in soup.find_all('a')]
    return urls

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def extract_base_url(url):
    up_to = list(find_all(url, "/"))[2] # third '/' in the url
    return url[:up_to]

# tests

def main():
    """
    Runs the script through
    """
    args = get_args()

    if args["interactive"]:
        save_args(args)
    # args = load_args()

    base_url = extract_base_url(args["website"])
    soup = get_soup_object(args["website"])
    urls = get_urls(base_url, soup)
    
    if args["output_file"] is not None:
        with open(args["output_file"], "w") as output:
            output.write('\n'.join(urls))
        return f"writen all links to {args['output_file']}"
    else:
        return urls


if __name__ == "__main__":
    main()
