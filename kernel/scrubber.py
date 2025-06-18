"""scrubber doc string"""

from __future__ import print_function
from pprint import pprint

from p4_scrubber.kernel.depots import (find_depot, delete_depot)
from p4_scrubber.kernel.streams import (find_streams_from_depot, delete_stream)
from p4_scrubber.kernel.shelves import (find_shelves_by_client, find_shelves_by_user, delete_shelf)
from p4_scrubber.kernel.users import (find_users_by_name, delete_users)
from p4_scrubber.kernel.clients import (find_clients_by_user, find_clients_by_stream, delete_clients)
from p4_scrubber.kernel.permissions import (find_permissions_by_depot, find_permissions_by_stream, delete_permissions)


def run_scrubber(server, manifest, dryrun=0):

    
    users_to_delete =  set(manifest.get("users", []))
    depots_to_delete = set(manifest.get("depots", []))
    streams_to_delete = set(manifest.get("streams", []))
    clients_to_delete = set(manifest.get("clients", []))
    shelves_to_delete = set(manifest.get("shelves", []))

    for user in users_to_delete:
        # gather clients from users
        user_clients = find_clients_by_user(server, user)
        clients_to_delete = clients_to_delete.union(user_clients)

        # gather shelves from users
        user_shelves = find_shelves_by_user(server, user)
        shelves_to_delete = shelves_to_delete.union(user_shelves)

    # gather streams from depots
    for depot in depots_to_delete:
        streams_to_delete = streams_to_delete.union(find_streams_from_depot(server, depot))
    

    # gather clients from streams
    for stream in streams_to_delete:
        stream_client_results = find_clients_by_stream(server, stream)
        clients_to_delete = clients_to_delete.union(stream_client_results)


    # gather shelves from clients
    for client in clients_to_delete:
        shelved_client_results = find_shelves_by_client(server, client)
        shelves_to_delete = shelves_to_delete.union(shelved_client_results)


    # gather permissions from depots
    # gather permissions from streams

    manifest['streams']= list(streams_to_delete)
    manifest['depots']= list(depots_to_delete)
    manifest['clients']= list(clients_to_delete)
    manifest['shelves']= list(shelves_to_delete)

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