#    p4templates - custom tooling to quickly create Helix Core depot/stream/group/permission setups.
#    Copyright (C) 2024 Perforce Software, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import print_function

import json
import re
import os

from P4 import P4


def load_server_config(config_path="config.json"):
    config = {}
    if validate_json(config_path):
        config =  read_json(config_path)
    return config


def setup_server_connection(port=None, user=None, password=None, charset="none"):
    if not (port and user):
        print("missing needed variable")
        print("port:", port)
        print("user:", user)
        return

    if not password:
        print("passwd:", password)
        print('Password not provided, attempting to use local ticket')

    p4 = P4()

    p4.charset = charset
    if password:
        p4.password = password
    p4.user = user
    p4.port = port

    p4.connect()
    if password:
        p4.run_login()

    return p4


def set_default(obj):
    """
    Converts any set to a list type object.
    """
    if isinstance(obj, set):
        return list(obj)
    return obj


def write_json(data_dict, output_path, sort_keys=False):
    """
    Writes a dictionary into a json file.
    """
    with open(output_path, "w") as outfile:
        json.dump(
            data_dict, outfile, default=set_default, indent=4, sort_keys=sort_keys
        )


def read_json(json_path):
    """
    Reads a json file in to a dictionary.
    """
    data_dict = {}
    with open(json_path) as json_file:
        data_dict = json.load(json_file)
    return data_dict


def validate_json(json_path):
    try:
        read_json(json_path)
    except Exception:
        print('JSON file read error:', json_path)
        return False
    return True


def convert_to_string(input, delimiter=" "):
    if isinstance(input, str):
        return input
    elif isinstance(input, (list, set)):
        return delimiter.join(sorted(input))
    elif isinstance(input, tuple):
        return delimiter.join(input)
    else:
        return str(input)
