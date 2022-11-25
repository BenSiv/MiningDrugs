"""
Scrapes all links from the website: https://www.drugs.com/
"""

# import modules
import sys
sys.path.insert(0, "src/")
import re
import toml
import logging

logging.basicConfig(
    filename="Drug.log",
    level=logging.DEBUG,
    format='%(levelname)s : %(asctime)s => %(message)s'
)

from scrape_links import scrape_links
from filter_links import filter_links
from scrape_page import scrape_page
from db_utils import *
from drug_classes import *


def find_between(s, first, last):
    """lets you retrive a string that sits beatween two other string"""
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def clean_attribute(attr_dict):
    """cleans each attribute"""
    cleaner_dict = {
        "title" : lambda a: a,
        "subtitle" : lambda a: re.sub(r'\[.+?\]', '',find_between(a, "\nGeneric name: ", "\n")).strip(),
        "related_treatments" : lambda a: a.split("\n"),
        "related_drugs" : lambda a: find_between(a, "\nRelated/similar drugs\n", "\n").split(",")
    }
    for key, value in attr_dict.items():
        attr_dict[key] = cleaner_dict[key](value)
    return attr_dict


def pack_drug(drug_dict):
    """takes clean drug attribute data and inserting it to drug info classes"""
    if "title" not in drug_dict:
        return None
    else:
        some_drug = Drug(drug_dict["title"], drug_dict.get("subtitle",""))
        medical_conditions = list()
        if "related_treatments" in drug_dict:
            for condition in drug_dict["related_treatments"]:
                if condition: # not empty string
                    medical_conditions.append(MedicalCondition(condition,""))
        side_effects = list()
        if "side_effects" in drug_dict:
            for side_effect in drug_dict["side_effects"]:
                if side_effect: # not empty string
                    side_effects.append(MedicalCondition(side_effect,""))
    return some_drug, medical_conditions, side_effects


def build_query(table, obj, credentials):
    """building insert query for mysql"""
    column_names = get_column_names(table, credentials)
    next_id = increment_id(table, credentials)
    attributes = get_class_attributes(type(obj))

    sql = f"""INSERT INTO {table} ("""
    col_count = 0
    while col_count < len(column_names):
        sql += f"{column_names[col_count]}, "
        col_count += 1
    sql = sql[:-2] + ") "
    
    sql += f"""VALUES ({next_id}, """
    attr_count = 0
    while attr_count < len(attributes):
        sql += f""""{getattr(obj,attributes[attr_count])}", """
        attr_count += 1
    sql = sql[:-2] + ");"
    
    return sql

def build_query_connective(table, obj1, obj2, credentials):
    """building insert query for mysql for connective table"""
    class_to_table = {"MedicalCondition" : "medical_conditions", "SideEffect" :  "side_effects"}
    column_names = get_column_names(table, credentials)
    next_id = increment_id(table, credentials)
    drug_id = get_id("drugs", obj1, credentials)
    related_id = get_id(class_to_table[type(obj2).__name__], obj2, credentials)

    sql = f"""INSERT INTO {table} ("""
    col_count = 0
    while col_count < len(column_names):
        sql += f"{column_names[col_count]}, "
        col_count += 1
    sql = sql[:-2] + ") "
    
    sql += f"""VALUES ({next_id}, """
    sql += f"{drug_id}, {related_id});"
    return sql


def insert_to_database(drug, medical_conditions, side_effects, credentials):
    """takes drug info classes and inserting it to the tables in the database"""
    # drug table
    query = build_query("drugs", drug, credentials)
    logging.info(f"sending query: {query}")
    send_query(query, credentials)

    # medical conditions
    for condition in medical_conditions:
        query = build_query("medical_conditions", condition, credentials)
        logging.info(f"sending query: {query}")
        send_query(query, credentials)

    # drug medical conditions
    for condition in medical_conditions:
        query = build_query_connective("drug_medical_conditions", drug, condition, credentials)
        logging.info(f"sending query: {query}")
        send_query(query, credentials)

    # side effect
    for effect in side_effects:
        query = build_query("side_effects", effect, credentials)
        logging.info(f"sending query: {query}")
        send_query(query, credentials)

    # drug side effect
    for effect in side_effects:
        query = build_query_connective("drug_side_effects", drug, effect, credentials)
        logging.info(f"sending query: {query}")
        send_query(query, credentials)
    
    # related drugs



def retrive_drug_info(links_file, attributes, credentials):
    """retrives drug info link by link, preccessing it and passing to the database"""
    with open(links_file, "r") as links:
        while True:
            line = links.readline()
            if not line:
                break
            else:
                raw_attr = scrape_page(attributes, line)
                attr = clean_attribute(raw_attr)
                drug, medical_conditions, side_effects = pack_drug(attr)
                insert_to_database(drug, medical_conditions, side_effects, credentials)


def scrape_drugs(attributes, links_file, credentials_file, only_part2=False):
    """
    The main function to retrive info from https://www.drugs.com
    """
    with open(credentials_file) as toml_file:
        credentials = toml.load(toml_file)

    if not only_part2:
        print("PART 1: saving all links")
        logging.info("scraping all links")
        mtm_links = scrape_links("https://www.drugs.com/mtm/")
        mtm_links_filtered = filter_links(mtm_links, "^https://www.drugs.com/mult")

        with open(links_file, "w") as output:
            for link in mtm_links_filtered:
                drug_links = scrape_links(link)
                drug_links_filtered = filter_links(drug_links, "^https://www.drugs.com/mtm(.*?)\.html$")
                output.write("\n".join(drug_links_filtered))

    print("PART 2: retriving all drugs info")
    retrive_drug_info(links_file, attributes, credentials)


def main():
    """runs tests"""
    pass


if __name__ == "__main__":
    attr_file = "configs/attributes.yaml"
    # links_file = "multum/all_drug_links.txt"
    links_file = "multum/test_drug_links.txt"
    credentials_file = "/home/bensiv/Documents/ITC/Main/MySql/mysql_credentials.toml"
    # saves to the database
    scrape_drugs(attr_file, links_file, credentials_file, only_part2=True)
