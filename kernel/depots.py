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


def validate_depot(server, depot_name):
    """find_depot doc string"""

    existing_depot_names = {_["Depot"] for _ in server.iterate_depots()}

    if depot_name not in existing_depot_names:
        print("Depot {} not found \n".format(depot_name))
        return False
    return True



def delete_depot(
    server, depot_name=None, dryrun=0
):
    """delete_depot doc string"""
    # p4 obliterate -y //depot_path/...
    
    depot_path = '//{}/...'.format(depot_name)
    
    if not dryrun:
        response = server.run('obliterate', '-y', '-h', depot_path)
        # response = server.stream( '-o' depot_path)
        print("response", response)
        response = server.delete_depot('-f', depot_name)
        print("response", response)
        # print('Deleted depot:', depot_name)
        return True
    else:
        print('Dry Run: would have deleted depot:', depot_name)

