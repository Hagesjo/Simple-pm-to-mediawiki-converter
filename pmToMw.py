#!/usr/bin/env python
# -*- coding: utf-8 -*-

import funcs

from ast import literal_eval


def parsePmDictFile(fileName):
    """
    Reads a pmwiki python dictionary file and for every revision in it parses the
    content and then returns the new dictionary with parsed content.
    """
    content = open(fileName, 'r').read()
    # Parsing strings can be dangerous, literal_eval to the rescue!
    dict = literal_eval(content)

    # Every i'nth element in the dictionary is a revision
    for i in dict:
        # Parse content
        dict[i]['content'] = funcs.parse(dict[i]['content'])

    return dict

def main(args):
    """
    Main function, calls parsePmDictFile and prints it.
    """
    newFile = parsePmDictFile(args[0])
    print(newFile)


# When running this file call main as function.
if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
