"""
Scrapes all links from the website: https://www.drugs.com/
"""

# import modules
import sys
sys.path.insert(0, "src/")

from scrape_links import scrape_links
from filter_links import filter_links
from scrape_page import scrape_page

def scrape_drugs(attributes, links_file, drugs_file=None, only_part2=False):
    """
    The main function to retrive info from https://www.drugs.com
    """
    if only_part2:
        pass
    else:
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
        with open(links_file, "r") as links:
            while True:
                line = links.readline()
                if not line:
                    break
                else:
                    results = scrape_page(attributes, line)    
                    if results is not None:
                        for key, value in results.items():
                            print(f"{key} : {value}\n")
                            print("-"*50)
                        print("="*50)
    else:
        print("PART 2: saving all drugs info")
        with open(links_file, "r") as links:
            while True:
                line = links.readline()
                if not line:
                    break
                else:
                    scrape_page(attributes, line, drugs_file)



if __name__ == "__main__":
    # print to screen
    print(scrape_drugs("configs/attributes.yaml", "multum/all_drug_links.txt", only_part2=True))#, "multum/all_drugs.jsonl")
    # save to file
    # scrape_drugs("attributes.yaml", "multum/all_drug_links.txt", "multum/all_drugs.jsonl", only_part2=True)
