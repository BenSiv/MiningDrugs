"""
Retrives medical conditions and side effects data from https://en.wikipedia.org
"""

import requests
import json

def get_description(term_query):
    base_url = "https://en.wikipedia.org/w/"
    query_url = base_url + f"api.php?action=query&exlimit=1&explaintext=1&exsentences=1&formatversion=2&prop=extracts&titles={term_query}&format=json"
    response = requests.get(query_url)
    response_dict = json.loads(response.content)
    pages = response_dict["query"]["pages"]
    if pages: # not empty list
        page_missing = pages[0].get("missing") # have a 'missing' key
        if page_missing is None:
            description = pages[0]["extract"] # get first sentence
            if description: # not an empty string
                return description

def main():
    terms = ["headache", "vomiting", "ulcerative colitis", "rectal bleeding", "headaches", "severe stomach pain"]
    for term in terms:
        print(get_description(term))

if __name__ == "__main__":
    main()
