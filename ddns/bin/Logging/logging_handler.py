#!python3
# Acts as functional entrypoint for this folder

import logging
import logging.handlers
import sys
# import syslog


def find_longest_path_in_project(project_path: str, file_extension: str = ".py"):
    import os
    import glob
    # project_path_and_bin = os.path.join(project_path+'/bin/')
    longest_path_length = 0

    # Use glob to find all Python scripts in the project
    search_pattern = os.path.join(project_path, f"**/*{file_extension}")
    python_files = glob.glob(search_pattern, recursive=True)

    for python_file in python_files:
        # python_file = python_file.removeprefix(project_path_and_bin)
        python_file = python_file.split('/')[-1]
        # Calculate the length of the path+filename
        file_length = len(python_file)
        # Update longest_path_length if the current file_length is greater
        longest_path_length = max(longest_path_length, file_length)

    return longest_path_length

def setup_logging(verbose: bool, debug: bool, project_path: str):
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    elif verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    format_string = "%(asctime)s %(process)s {location}%(levelname)-7s: %(message)s"
    if logger.level < logging.INFO:
        longest_py_path = find_longest_path_in_project(project_path)
        # longest_py_path = 10
        location = f"%(filename)-{longest_py_path}s %(funcName)16s:%(lineno)-3s "
        format_string = format_string.format(location=location)
    else:
        format_string = format_string.format(location="")

    formatter = logging.Formatter(format_string)

    # Create a handler that writes log messages to stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    # Make the requests library (urllib3) calm down
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # # Set the logging level for the asyncio logger to WARNING
    # asyncio_logger = logging.getLogger("asyncio")
    # asyncio_logger.setLevel(logging.WARNING)