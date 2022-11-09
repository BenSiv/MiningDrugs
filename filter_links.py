"""
Filters a file of links based on presence of string
"""

# import modules
import argparse
import toml

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

# def filter_links(file, query, output):
#     """filters all links in file"""
#     with open(output, "w") as output_file:
#         with open(file) as input_file:
#             for line in input_file.readlines():
#                 if query in line:
#                     output_file.write(line)


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

def filter_links(file, query):
    with open(file) as f:
        link_gen = lazy_filter(f, query)
        return list(link_gen)


# tests

def main():
    """
    Runs the script through
    """
    args = get_args()

    if args["interactive"]:
        save_args(args)
    # args = load_args()

    # filter_links(args["input_file"], args["query"], args["output_file"])
    
    # links_filtered = filter_links("multum/mtm_links.txt", "mult")
    if args["output_file"] is not None:
        with open(args["output_file"], "w") as output:
            for filtered_link in filter_links("multum/mtm_links.txt", "mult"):
                output.write(filtered_link)
        return f"writen all links to {args['output_file']}"
    else:
        print(*filter_links("multum/mtm_links.txt", "mult"))

        

if __name__ == "__main__":
    main()
