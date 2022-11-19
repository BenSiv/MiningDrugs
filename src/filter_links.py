"""
Filters a file of links based on presence of string
"""

# import modules
import argparse
from cmd_args import save_args, load_args
import re

# argparse function
def get_args(argv=None):
    """
    Takes arguments from the user when running as a command line script
    """
    parser = argparse.ArgumentParser(description="Scraping all links from a given website")
    parser.add_argument("-f","--input_file", help="file of links", required=True)
    parser.add_argument("-q","--query", help="substring to search", required=True)
    parser.add_argument("-o","--output_file", help="name of the file to save the output")
    parser.add_argument("-i", "--interactive", action="store_true", help="saves all the arguments to CmdArgs.yaml")
    parser.add_argument("-t", "--tests", action="store_true", help="runs tests for this script")
    return vars(parser.parse_args(argv))


def lazy_filter(input_file, query):
    """filters all links in file"""
    line = "true"
    while True:
        line = input_file.readline()
        if not line:
            break
        else:
            if query in line:
                yield line

def filter_from_file(file, query):
    with open(file) as f:
        link_gen = lazy_filter(f, query)
        return list(link_gen)


def filter_links(links, query, output_file=None):
    """
    Wrapper function to call as module.function
    """
    
    if output_file is not None:
        with open(output_file, "w") as output:
            for link in links:
                # if query in link:
                if re.match(query, link) is not None:
                    output.write(link)
    else:
        result = list()
        for link in links:
                if re.match(query, link) is not None:
                    result.append(link)
        return result
                 

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


    if args["output_file"] is not None:
        with open(args["output_file"], "w") as output:
            for filtered_link in filter_from_file("multum/mtm_links.txt", "mult"):
                output.write(filtered_link)
        return f"writen all links to {args['output_file']}"
    else:
        print(*filter_from_file("multum/mtm_links.txt", "mult"))

        

if __name__ == "__main__":
    main()
