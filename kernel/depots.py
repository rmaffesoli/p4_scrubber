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

from __future__ import print_function


def find_depot(
    server, depot_name=None, dryrun=0
):
    """find_depot doc string"""

    existing_depot_names = {_["Depot"] for _ in server.iterate_depots()}

    if depot_name not in existing_depot_names:
        print("Depot {} not found \n".format(depot_name))
        return

    depot_spec = server.fetch_depot(depot_name)

    if dryrun:
        print("-" * 20, "\n")
        print(depot_spec, "\n")
        print("-" * 20, "\n")
    return depot_spec


def delete_depot(
    server, depot_name=None, dryrun=0
):
    """delete_depot doc string"""
    print('Not implemented')
    return

if __name__ == "__main__":
    from utils import setup_server_connection
    server = setup_server_connection(
        port="ssl:helix:1666", user="rmaffesoli"
    )

    depot = find_depot(server=server, depot_name="delete_me_stream", dryrun=1)


