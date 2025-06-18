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


def delete_stream(
    # p4 stream -f --obliterate -y name@change
):
    pass


if __name__ == "__main__":
    from utils import setup_server_connection
    server = setup_server_connection(
        port="ssl:helix:1666", user="rmaffesoli"
    )

    depot = find_streams_from_depot(server=server, depot_name="delete_me_stream", dryrun=1)

