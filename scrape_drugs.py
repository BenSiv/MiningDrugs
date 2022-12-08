"""
Scrapes all links from the website: https://www.drugs.com/
"""

# import modules
import sys
sys.path.insert(0, "src/")
import argparse
import re
import toml
import logging

logging.basicConfig(
    filename="Drug.log",
    level=logging.DEBUG,
    format='%(levelname)s : %(asctime)s => %(message)s'
)

from cmd_args import save_args, load_args
from scrape_links import scrape_links
from filter_links import filter_links
from scrape_page import scrape_page
from wikipedia_api import get_description
from db_utils import *
from drug_classes import *

# argparse function
def get_args(argv=None):
    """
    Takes arguments from the user when running as a command line script
    """
    parser = argparse.ArgumentParser(description="Scraping all links from a given website")
    parser.add_argument("-w","--website", help="website to scrape")
    parser.add_argument("-l","--links", help="file with all links of website to scrape from")
    parser.add_argument("-a","--attributes", help="yaml file for the attributes to scrape", required=True)
    parser.add_argument("-c","--credentials", help="toml file with the credential for the MySQL connection", required=True)
    parser.add_argument("--only_part2", action="store_true", help="yaml file fore the attributes to scrape")
    parser.add_argument("-i", "--interactive", action="store_true", help="saves all the arguments to CmdArgs.yaml")
    parser.add_argument("-t", "--tests", action="store_true", help="runs tests for this script")
    return vars(parser.parse_args(argv))


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
    def clean_subtitle(subtitle):
        generic_name = find_between(subtitle, "\nGeneric name: ", "\n")
        return re.sub(r'\[.+?\]', '',generic_name).strip()

    def clean_side_effect(side_effect):
        after = "Common side effects of"
        before = "This is not a complete list of side effects"
        side_effect = find_between(side_effect, after, before)
        side_effect_list = side_effect.split("\n\n\n")[1:-1]
        side_effect_list = re.split("\n\n\n|,", side_effect)[1:-1]

        results = list()
        for se in side_effect_list:
            se = re.sub(r'\[.+?\]', '',se).strip()
            se = re.sub('; or', '',se)
            results.append(se)
        return results

    def clean_related_drugs(related_drug):
        after = "\nRelated/similar drugs\n"
        before = "\n"
        related_drug = find_between(related_drug, after, before)
        related_drug_list = related_drug.split(", ")

        results = list()
        for rd in related_drug_list:
            rd = re.sub(r'\[.+?\]', '',rd).strip()
            rd = re.sub('; or', '',rd)
            results.append(rd)
        return results

    cleaner_dict = {
        "title" : lambda a: a,
        "subtitle" : lambda a: clean_subtitle(a),
        "related_treatments" : lambda a: a.split("\n"),
        "side_effects" : lambda a: clean_side_effect(a),
        "related_drugs" : lambda a: clean_related_drugs(a)
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
                    description = get_description(condition)
                    if description is not None:
                        description = description.split("\n")[0]
                    medical_conditions.append(MedicalCondition(condition, description))
        side_effects = list()
        if "side_effects" in drug_dict:
            for side_effect in drug_dict["side_effects"]:
                if side_effect: # not empty string
                    description = get_description(side_effect)
                    if description is not None:
                        description = description.split("\n")[0]
                    side_effects.append(SideEffect(side_effect, description))
        related_drugs = list()
        if "related_drugs" in drug_dict:
            for related_drug in drug_dict["related_drugs"]:
                if related_drug: # not empty string
                    related_drugs.append(Drug(related_drug,""))
    return some_drug, medical_conditions, side_effects, related_drugs


def build_query(table, obj, connection):
    """building insert query for mysql"""
    column_names = get_column_names(table, connection)
    next_id = increment_id(table, connection)
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

def build_query_connective(table, obj1, obj2, connection):
    """building insert query for mysql for connective table"""
    class_to_table = {"Drug" : "drugs", "MedicalCondition" : "medical_conditions", "SideEffect" :  "side_effects"}
    column_names = get_column_names(table, connection)
    next_id = increment_id(table, connection)
    drug_id = get_id("drugs", obj1, connection)
    related_id = get_id(class_to_table[type(obj2).__name__], obj2, connection)

    sql = f"""INSERT INTO {table} ("""
    col_count = 0
    while col_count < len(column_names):
        sql += f"{column_names[col_count]}, "
        col_count += 1
    sql = sql[:-2] + ") "
    
    sql += f"""VALUES ({next_id}, """
    sql += f"{drug_id}, {related_id});"
    return sql

def update_query(table, obj, connection):
    """building update query for mysql"""
    column_names = get_column_names(table, connection)
    id = get_id(table, obj, connection)
    attributes = get_class_attributes(type(obj))

    sql = f"""UPDATE {table} """    
    sql += f"""SET """
    attr_count = 0
    while attr_count < len(attributes):
        sql += f"{column_names[attr_count+1]}="
        sql += f""""{getattr(obj,attributes[attr_count])}", """
        attr_count += 1
    sql = sql[:-2]
    
    sql += f""" WHERE id={id};"""
    return sql

def exists_in_database(table, obj, connection):
    """checks if element has entry in database table"""
    obj_id = get_id(table, obj, connection)
    if obj_id is not None:
        return True
    else:
        return False

def insert_to_database(drug, medical_conditions, side_effects, related_drugs, connection):
    """takes drug info classes and inserting it to the tables in the database"""

    # drug table
    if not exists_in_database("drugs", drug, connection):
        query = build_query("drugs", drug, connection)
        logging.info(f"sending query: {query}")
        send_query(query, connection)
    else:
        query = update_query("drugs", drug, connection)
        logging.info(f"sending query: {query}")
        send_query(query, connection)

    # medical conditions
    for condition in medical_conditions:
        if not exists_in_database("medical_conditions", condition, connection):
            query = build_query("medical_conditions", condition, connection)
            logging.info(f"sending query: {query}")
            send_query(query, connection)

    # drug medical conditions
    for condition in medical_conditions:
        query = build_query_connective("drug_medical_conditions", drug, condition, connection)
        logging.info(f"sending query: {query}")
        send_query(query, connection)

    # side effect
    for effect in side_effects:
        if not exists_in_database("side_effects", effect, connection):
            query = build_query("side_effects", effect, connection)
            logging.info(f"sending query: {query}")
            send_query(query, connection)

    # drug side effect
    for effect in side_effects:
        query = build_query_connective("drug_side_effects", drug, effect, connection)
        logging.info(f"sending query: {query}")
        send_query(query, connection)
    
    # related drugs
    for rdrug in related_drugs:
        if not exists_in_database("drugs", rdrug, connection):
            query = build_query("drugs", rdrug, connection)
            logging.info(f"sending query: {query}")
            send_query(query, connection)
        query = build_query_connective("related_drugs", drug, rdrug, connection)
        logging.info(f"sending query: {query}")
        send_query(query, connection)
    



def retrive_drug_info(links_file, attributes, connection):
    """retrives drug info link by link, preccessing it and passing to the database"""
    with open(links_file, "r") as links:
        while True:
            line = links.readline()
            if not line:
                break
            else:
                raw_attr = scrape_page(attributes, line)
                attr = clean_attribute(raw_attr)
                drug, medical_conditions, side_effects, related_drugs = pack_drug(attr)
                insert_to_database(drug, medical_conditions, side_effects, related_drugs, connection)


def scrape_drugs(attributes, links_file, credentials_file, only_part2=False):
    """
    The main function to retrive info from https://www.drugs.com
    """
    with open(credentials_file) as toml_file:
        credentials = toml.load(toml_file)

    connection = connect(credentials)

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
    retrive_drug_info(links_file, attributes, connection)


def main():
    """runs tests"""
    args = get_args()

    if args["interactive"]:
        save_args(args)
    # args = load_args()

    scrape_drugs(args["attributes"], args["links"], args["credentials"], args["only_part2"])


if __name__ == "__main__":
    main()
    # python scrape_drugs.py \
    #   -a "configs/attributes.yaml" \
    #   -c "/home/bensiv/Documents/ITC/Main/MySql/mysql_credentials.toml"
    #   -l "multum/test_drug_links.txt"
    #   --only_part2

    # attr_file = "configs/attributes.yaml"
    # links_file = "multum/all_drug_links.txt"
    # links_file = "multum/test_drug_links.txt"
    # credentials_file = "/home/bensiv/Documents/ITC/Main/MySql/mysql_credentials.toml"
