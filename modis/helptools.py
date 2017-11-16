from collections import OrderedDict
import json as _json

import logging

logger = logging.getLogger(__name__)


def get_help_data(filepath):
    """
    Get the json data from a help file

    Args:
        filepath (str): The file path for the help file

    Returns:
        data: The json data from a help file
    """

    try:
        with open(filepath, 'r') as file:
            return _json.load(file, object_pairs_hook=OrderedDict)
    except Exception as e:
        logger.error("Could not load file {}".format(filepath))
        logger.exception(e)
        return {}


def get_help_datapacks(filepath, prefix="!"):
    """
    Load help text from a file and give it as datapacks

    Args:
        filepath (str): The file to load help text from
        prefix (str): The prefix to use for commands

    Returns:
        datapacks (list): The datapacks from the file
    """

    help_contents = get_help_data(filepath)

    datapacks = []

    # Add the content
    for d in help_contents:
        heading = d
        content = ""

        if d == "Commands":
            for c in help_contents[d]:
                if "name" not in c:
                    continue

                content += "`"
                command = prefix + c["name"]
                content += "{}".format(command)
                if "params" in c:
                    for param in c["params"]:
                        content += " [{}]".format(param)
                content += "`: "
                if "description" in c:
                    content += c["description"]
                content += "\n"
        else:
            content += help_contents[d]

        datapacks.append((heading, content, True))

    return datapacks


def add_help_text(parent, filepath, prefix="!"):
 
