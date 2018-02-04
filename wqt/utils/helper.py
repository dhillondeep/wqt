"""@package utils
Helper functions to be used through the tool
"""

import os
from os.path import abspath, dirname
import shutil

from six import string_types


def quote_join(values):
    """Join a set of strings, presumed to be file paths, surrounded by quotes, for CMake"""

    surrounded = []
    for value in values:
        surrounded.append('\"' + value + '\"')
    return ' '.join(surrounded)


def linux_path(path):
    """Converts Windows style path to linux style path"""

    return os.path.abspath(path).replace('\\', '/')


def get_wqt_path():
    """returns the absolute path of wcosa"""

    wcosa_path = dirname(abspath(__file__))
    return linux_path(dirname(dirname(wcosa_path)))


def get_cmake_path():
    """returns the absolute path of cosa"""

    return linux_path(get_wqt_path() + '/toolchain/cmake')


def get_working_directory():
    """get path from where the script is called"""

    return linux_path(os.path.abspath(os.getcwd()))


def fill_template(string, data):
    """Fills the template based on the data provided"""

    string = string.replace('\\n', '\n').replace('\\t', '\t')

    for key in data:
        value = str(data[key])

        if isinstance(data[key], list):
            value = ' '.join(data[key])
        elif isinstance(data[key], string_types):
            value = data[key]

        if '{{' + key + '}}' in string:
            return string.replace('{{' + key + '}}', value)

    return string


def create_folder(path, override=False):
    """Creates a folder at the given path"""

    if override:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
    elif not os.path.exists(path):
        os.mkdir(path)


def get_files_recursively(directory, extensions=None):
    """gathers a list of all the files with the extensions recursively in a directory"""

    arr = []
    for root, dirs, files in os.walk(directory):
        path = root.split(os.sep)
        for file in files:
            ext = os.path.splitext(file)[1]

            if extensions is not None and ext in extensions:
                arr.append(linux_path('/'.join(path) + '/' + file))
            elif extensions is None:
                arr.append(linux_path('/'.join(path) + '/' + file))

    return arr


def get_files(path, extensions=None):
    """gathers a list of all the files with the extensions in a directory"""

    arr = []
    all_files = os.listdir(path)

    for file in all_files:
        if not os.path.isdir(path + '/' + file) and extensions is not None and os.path.splitext(file)[1] in extensions:
            arr.append(linux_path(path + '/' + file))
        elif not os.path.isdir(path + '/' + file) and extensions is None:
            arr.append(linux_path(path + '/' + file))

    return arr


def get_dirs_recursively(path):
    """gathers a list of all the subdirectories recursively inside the path"""

    arr = []
    for root, dirs, files in os.walk(path):
        curr_path = '/'.join(root.split(os.sep))

        if curr_path != os.path.basename(path):
            arr.append(linux_path(curr_path))

    return arr


def get_dirs(path):
    """gathers a list of all the subdirectories inside the path"""

    arr = []
    for file in os.listdir(path):
        if os.path.isdir(path + '/' + file):
            arr.append(linux_path(path + '/' + file))

    return arr


def get_dirnames(path):
    """gathers a list of all the names of subdirectories inside the path"""

    arr = []
    for file in os.listdir(path):
        if os.path.isdir(path + '/' + file):
            arr.append(os.path.basename(linux_path(path + '/' + file)))

    return arr
