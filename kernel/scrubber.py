"""scrubber doc string"""

from __future__ import print_function
from pprint import pprint

from p4_scrubber.kernel.depots import (find_depot, delete_depot)
from p4_scrubber.kernel.streams import (find_streams_from_depot, delete_stream)
from p4_scrubber.kernel.shelves import (find_shelves_by_client, delete_shelf)
from p4_scrubber.kernel.users import (find_users_by_name, delete_users)
from p4_scrubber.kernel.clients import (find_clients_by_user, find_clients_by_stream, delete_clients)
from p4_scrubber.kernel.permissions import (find_permissions_by_depot, find_permissions_by_stream, delete_permissions)


def run_scrubber(server, manifest, dryrun=0):
    # gather clients from users
    # gather shelves from users
    
    # gather streams from depots
    depots_to_delete = set(manifest.get("depots", []))
    streams_to_delete = set(manifest.get("streams", []))
    clients_to_delete = set(manifest.get("clients", []))


    for depot in depots_to_delete:
        streams_to_delete = streams_to_delete.union(find_streams_from_depot(server, depot))
    

    # gather permissions from depots
    # gather clients from streams
    
    for stream in streams_to_delete:
        stream_client_results = find_clients_by_stream(server, stream)
        print(stream, stream_client_results)
        clients_to_delete = clients_to_delete.union(find_clients_by_stream(server, stream))

    # gather permissions from streams

    manifest['streams']= list(streams_to_delete)
    manifest['depots']= list(depots_to_delete)
    manifest['clients']= list(clients_to_delete)

    if dryrun:
        pprint(manifest)
    else:
        pass
        # delete the damn things
        # delete_shelves
        # delete_clients
        # delete_streams
        # delete_depots
        # delete_users

    return manifest


if __name__ == "__main__":
    from utils import setup_server_connection
    server = setup_server_connection(
        port="ssl:helix:1666", user="rmaffesoli"
    )

    manifest = {
        "depots": ["delete_me_stream"],
        "streams": ["placeholder"],
    }

    run_scrubber(server, manifest, dryrun=1)