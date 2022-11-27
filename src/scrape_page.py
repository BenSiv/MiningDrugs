"""
Scrapes page for selected elements
"""

# import modules
import argparse
import yaml
import requests
from bs4 import BeautifulSoup
from cmd_args import save_args, load_args
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}

# argparse function
def get_args(argv=None):
    """
    Takes arguments from the user when running as a command line script
    """
    parser = argparse.ArgumentParser(description="Scraping all links from a given website")
    parser.add_argument("-w","--website", help="website to scrape", required=True)
    parser.add_argument("-a","--attributes", help="yaml file fore the attributes to scrape", required=True)
    parser.add_argument("-o","--output_file", help="name of the file to save the output")
    parser.add_argument("-i", "--interactive", action="store_true", help="saves all the arguments to CmdArgs.yaml")
    parser.add_argument("-t", "--tests", action="store_true", help="runs tests for this script")
    return vars(parser.parse_args(argv))


def get_soup_object(URL):
    """
    Send a request to a page and return the response as a BeautifulSoup object
    """
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content , 'html.parser')
    return soup


def get_content(soup):
    """
    Returns the content part of soup object
    """
    content = soup.find(id="content")
    return content.find("div", class_="contentBox")


def read_attributes(attr_file):
    """reads attribute from a yaml file"""
    with open(attr_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def get_attributes(attr_list, soup_info):
    """reads attribute content from soup object"""
    results = dict()
    for attr in attr_list:
        if attr["class"] is not None:
            info = soup_info.find(attr["section"], class_=attr["class"])
        else:
            if attr["name"] == "side_effects":
                info = soup_info
            else:
                info = soup_info.find(attr["section"])
        if info is not None:
            results[attr["name"]] = info.text
    return results


def scrape_page(attr_file, url):
    """retrive info from page based on attribute file"""
    soup = get_soup_object(url)
    info = get_content(soup)
    attr_list = read_attributes(attr_file)
    results = get_attributes(attr_list, info)
    return results


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

    results = scrape_page(args["attributes"], args["website"])
    if results is not None:
        for key, value in results.items():
            print(f"{key} : {value}\n")




if __name__ == "__main__":
    main()


