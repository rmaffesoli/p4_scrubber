#!/usr/bin/env python

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

"""create_stream doc string"""

from __future__ import print_function

def validate_stream(server, stream_name):
    existing_stream_names = {_['Stream'] for _ in server.iterate_streams()}
    if stream_name not in existing_stream_names:
        print("Stream {} not found \n".format(stream_name))
        return False
    return True

def find_streams_from_depot(
    server,
    depot_name=None,
):
    """create_stream doc string"""

    existing_stream_names = {_['Stream'] for _ in server.iterate_streams()}
    filtered_existing_stream_names= {_ for _ in existing_stream_names if "//{}/".format(depot_name) in _}

    return filtered_existing_stream_names


def sort_stream_tiers(server, streams_list):
    filtered_streams_list = [_ for _ in streams_list if validate_stream(server, _)]
    stream_sort_dict = {_:set() for _ in filtered_streams_list}
    stream_tier_dict = {}

    for stream_name in filtered_streams_list:
        stream_spec = server.fetch_stream(stream_name)

        parent = stream_spec.get('Parent', None)

        if parent and parent != 'none':
            if parent in stream_sort_dict:
                stream_sort_dict[parent].add(stream_name)

    while True:
        change_made = 0
        for parent, children in stream_sort_dict.items():
            for child in children:
                if stream_sort_dict[child]:
                    initial_parent_len = len(stream_sort_dict[parent])
                    stream_sort_dict[parent] =  stream_sort_dict[parent].union(stream_sort_dict[child])
                    new_parent_len = len(stream_sort_dict[parent])
                    if new_parent_len != initial_parent_len:
                        change_made = 1
        if not change_made:
            break   
    
    for stream, children in stream_sort_dict.items():
        num_children = len(children)
        if not num_children in stream_tier_dict:
            stream_tier_dict[num_children] = set()
        stream_tier_dict[num_children].add(stream)

    return stream_tier_dict


def delete_stream(server, stream, dryrun=0):
    # p4 stream -f --obliterate -y name@change
    if dryrun:
        result = "Would have deleted stream: {}".format(stream)
    else:
        result = server.run('stream', '-f', '--obliterate', '-y', stream)

    if isinstance(result, list):
        result = result[0]

    print(result)
    return result

