"""
Scrapes all links from the website: https://www.drugs.com/
"""

# import modules
import sys
sys.path.insert(0, "src/")
import os.path

from scrape_links import scrape_links
from filter_links import filter_links
from scrape_page import scrape_page
from db_utils import connect, send_query
import jsonlines

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def clean_attribute(attr_dict):
    cleaner_dict = {
        "title" : lambda a: a,
        "subtitle" : lambda a: find_between(a, "\nGeneric name: ", "\n"),
        "related_treatments" : lambda a: a.split("\n"),
        "related_drugs" : lambda a: find_between(a, "\nRelated/similar drugs\n", "\n").split(",")
    }

    for key, value in attr_dict.items():
        attr_dict[key] = cleaner_dict[key](value)

    return attr_dict


def terminal_dump(in_dict):
    """prints all drugs info to stdout"""
    for key, value in in_dict.items():
        print(f"{key} : {value}\n")
        print("-"*50)
    print("="*50)

def jsonl_dump(in_dict, output_file):
    """writes all drugs info to jsonl file"""
    if not os.path.isfile(output_file):
        print(f"{output_file} not found")
    else:
        with jsonlines.open(output_file, mode='a') as writer:
            writer.write(in_dict)


def retrive_drug_info(links_file, attributes, action="print", drugs_file=None, db_info=None):
    with open(links_file, "r") as links:
        while True:
            line = links.readline()
            if not line:
                break
            else:
                results = scrape_page(attributes, line)
                results = clean_attribute(results)

                if results is not None:
                    if action == "print":
                        terminal_dump(results)
                    elif action == "database":
                        if not isinstance(db_info, dict):
                            print("db_info must be a dictionary")
                        else:
                            send_query(db_info["sql"], db_info["credentials"])
                    elif action == "jsonl":
                        jsonl_dump(results, drugs_file)
                    else:
                        print(f"The action {action} is not known")


def scrape_drugs(attributes, links_file, drugs_file=None, only_part2=False):
    """
    The main function to retrive info from https://www.drugs.com
    """
    if not only_part2:
        print("PART 1: saving all links")
        mtm_links = scrape_links("https://www.drugs.com/mtm/")
        mtm_links_filtered = filter_links(mtm_links, "^https://www.drugs.com/mult")

        with open(links_file, "w") as output:
            for link in mtm_links_filtered:
                drug_links = scrape_links(link)
                drug_links_filtered = filter_links(drug_links, "^https://www.drugs.com/mtm(.*?)\.html$")
                output.write("\n".join(drug_links_filtered))

    if drugs_file is None:
        print("PART 2: retriving all drugs info")
        retrive_drug_info(links_file, attributes)
    else:
        retrive_drug_info(links_file, attributes, drugs_file)



if __name__ == "__main__":
    output_file = "multum/all_drugs.jsonl"
    attr_file = "configs/attributes.yaml"
    links_file = "multum/all_drug_links.txt"
    # print to screen
    print(scrape_drugs(attr_file, links_file, only_part2=True))
    # save to file
    # scrape_drugs(attr_file, links_file, output_file, only_part2=True)
