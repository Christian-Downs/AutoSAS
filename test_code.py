from configparser import ConfigParser
import os
import logging
import subprocess
import re
from updater import updater
from flask_logger import get_logger  # Import the function from logging.py

# read config file with 'General' section
config = ConfigParser()
config.read('config.ini')

port = config.get('General', 'port', fallback='5000')

logging = get_logger(flask_url=f"http://127.0.0.1:{port}/set_logging")  # Get the configured logger

def find_files(root_dir, filename):
    """
    Recursively searches for a file in a directory and its subdirectories.

    Args:
        root_dir (str): The root directory to start the search from.
        filename (str): The name of the file to search for.

    Returns:
        list: A list of absolute paths to the found files, or an empty list if not found.
    """
    results = []
    for root, _, files in os.walk(root_dir):
        if filename in files:
            results.append(os.path.join(root, filename))
    return results


# Remove file paths higher than project_root from traceback
def modify_traceback(tb, project_root):
    # Split the traceback by line and modify each line
    tb_lines = tb.splitlines()
    modified_tb = []

    for line in tb_lines:
        if project_root in line:
            # Keep everything from "output" onward
            line = line.split(project_root, 1)[-1]
        modified_tb.append(line)

    return "\n".join(modified_tb)


def tester():
    timeout = int(config.get('Generation', 'timeout', fallback='5'))
    max_tries = int(config.get('Generation', 'num_tries'))
    output_dir = config.get('Generation', 'output_dir')
    py_source_files = config.get('Generation', 'py_source_files').split(',')

    tries_counter = 0

    while tries_counter < max_tries:
        python_source = ""

        # check if we have a valid python source file (in order specified in config)
        for file in py_source_files:
            # search output directory recursively for file=main.py (for example)
            paths = find_files(output_dir, file)

            # no file found, continue to next possible filename
            if len(paths) == 0:
                continue
            elif len(paths) > 1:
                logging.warning(f'Multiple files found with name {file} in {output_dir}. Taking first one.')

            python_source = paths[0]

        # if we don't have a valid python source file, we try to generate one
        if python_source == "":
            logging.warning('No python source files found with names {py_source_files} in {output_dir}')
            # TODO: tell GPT to generate a valid app.py or main.py file to run

            tries_counter += 1
            continue

        # read stdout and stderr from python_source
        logging.info(f'Running {python_source}...')

        command = f'python3 {python_source}'

        # run the python source file
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # since we're running a server, it will run indefinitely
        # if it still hasn't thrown errors after 5 seconds, terminate it
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            logging.warning(f'Terminating {python_source} after {timeout} seconds...')
            process.terminate()
            process.wait()

        stdout, stderr = [s.decode() for s in process.communicate()]
        stdout = stdout.strip()
        stderr = modify_traceback(stderr.strip(), output_dir)

        print(stderr)

        if process.returncode == 0:
            logging.info(f'{python_source} ran successfully')
            return True
        # check if errors...
        else:
            logging.warning(f'Error running {python_source}')
            # Tell GPT to fix the error in the python_source file
            # stdout is the output of the program
            # stdderr has the entire error output
            # error_name is the name of the error
            # line_number is the line number that caused the error
            # error_message is the error message (last line of stderr)
            updater(stderr.strip())

            tries_counter += 1

    logging.error(f'Failed to run {python_source} after {max_tries} tries')
    return False

if __name__ == '__main__':
    tester()
