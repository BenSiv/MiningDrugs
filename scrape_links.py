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
    page = requests.get(URL)
    soup = BeautifulSoup(page.content , 'html.parser')
    return soup
    
def get_classes(soup):
    class_list = set()
    tags = {tag.name for tag in soup.find_all()}
    for tag in tags:
        for i in soup.find_all(tag):
            if i.has_attr( "class" ):
                if len( i['class'] ) != 0:
                    class_list.add(" ".join(i['class']))

    return class_list

def get_urls(soup):
    urls = [link.get('href') for link in soup.find_all('a')]
    return urls


# tests

def main():
    """
    Runs the script through
    """
    args = get_args()

    if args["interactive"]:
        save_args(args)
    # args = load_args()

    soup = get_soup_object(args["website"])
    urls = get_urls(soup)
    
    # get_classes(soup)
    # find_element = soup.find_all(class_="homeMain")
    
    return urls



if __name__ == "__main__":
    print(main())
