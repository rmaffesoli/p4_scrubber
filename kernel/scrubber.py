"""scrubber doc string"""

from __future__ import print_function
from pprint import pprint

from p4_scrubber.kernel.depots import (validate_depot, delete_depot)
from p4_scrubber.kernel.streams import (validate_stream, find_streams_from_depot, sort_stream_tiers, delete_stream)
from p4_scrubber.kernel.shelves import (validate_shelve, find_shelves_by_client, find_shelves_by_user, delete_shelf)
from p4_scrubber.kernel.users import (validate_user, delete_user)
from p4_scrubber.kernel.groups import (validate_group, delete_group)
from p4_scrubber.kernel.clients import (validate_client, find_clients_by_user, find_clients_by_stream, delete_client)
from p4_scrubber.kernel.permissions import (validate_permission, find_permissions_by_depot, find_permissions_by_stream, get_protections_table, delete_permission)


def run_scrubber(server, manifest, dryrun=0):
    users_to_delete =  set(manifest.get("users", []))
    depots_to_delete = set(manifest.get("depots", []))
    streams_to_delete = set(manifest.get("streams", []))
    clients_to_delete = set(manifest.get("clients", []))
    shelves_to_delete = set(manifest.get("shelves", []))
    groups_to_delete = set(manifest.get("groups", []))
    permissions_to_delete = manifest.get("permissions", [])

    users_to_delete = {_ for _ in users_to_delete if validate_user(server, _)}
    for user in users_to_delete:
        # gather clients from users
        user_clients = find_clients_by_user(server, user)
        clients_to_delete = clients_to_delete.union(user_clients)

        # gather shelves from users        
        shelves_to_delete = {_ for _ in shelves_to_delete if validate_shelve(server, _)}
        user_shelves = find_shelves_by_user(server, user)
        shelves_to_delete = shelves_to_delete.union(user_shelves)

    # gather streams from depots
    depots_to_delete = {_ for _ in depots_to_delete if validate_depot(server, _)}
    for depot in depots_to_delete:
        streams_to_delete = streams_to_delete.union(find_streams_from_depot(server, depot))
        
    # gather clients from streams
    streams_to_delete = {_ for _ in streams_to_delete if validate_stream(server, _)}
    for stream in streams_to_delete:
        stream_client_results = find_clients_by_stream(server, stream)
        clients_to_delete = clients_to_delete.union(stream_client_results)

    # gather shelves from clients
    clients_to_delete = {_ for _ in clients_to_delete if validate_client(server, _)}
    for client in clients_to_delete:
        shelved_client_results = find_shelves_by_client(server, client)
        shelves_to_delete = shelves_to_delete.union(shelved_client_results)


    existing_protections_list = get_protections_table(server)
    permissions_to_delete = [_ for _ in permissions_to_delete if validate_permission(existing_protections_list, _)]

    # gather permissions from depots
    for depot in depots_to_delete:
        depot_protections = find_permissions_by_depot(existing_protections_list, depot)
        for protection in depot_protections:
            if protection not in permissions_to_delete:
                permissions_to_delete.append(protection)

    # gather permissions from streams
    for stream in streams_to_delete:
        stream_protections = find_permissions_by_stream(existing_protections_list, stream)
        for protection in stream_protections:
            if protection not in permissions_to_delete:
                permissions_to_delete.append(protection)
    
    groups_to_delete = {_ for _ in groups_to_delete if validate_group(server, _)}

    manifest['users']= list(users_to_delete)
    manifest['depots']= list(depots_to_delete)
    manifest['streams']= list(streams_to_delete)
    manifest['clients']= list(clients_to_delete)
    manifest['shelves']= list(shelves_to_delete)
    manifest['groups']= list(groups_to_delete)
    manifest['permissions']= list(permissions_to_delete)

    # delete the damn things
    
    # delete_shelves
    for changelist in manifest.get('shelves', []):
        delete_shelf(server, changelist, dryrun)

    # delete_clients
    for changelist in manifest.get('clients', []):
        delete_client(server, client, dryrun)

    # delete_streams
    stream_tier_dict = sort_stream_tiers(server, manifest.get('streams', []))
    
    for tier in sorted(stream_tier_dict.keys()):
        for stream in stream_tier_dict[tier]:
            print(tier, stream)
            delete_stream(server, stream, dryrun)

    # delete_depots
    for depot_name in manifest.get('depots', []):
        delete_depot(server, depot_name, dryrun)

    # delete_groups
    for group_name in manifest.get('groups', []):
        delete_group(server, group_name, dryrun)
    
    # delete_users
    for user_name in manifest.get('users', []):
        delete_user(server, user_name, dryrun)
    
    # delete permissions
    # for permission in manifest.get('permissions', []):
    #     delete_permission(server, permission, dryrun)

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

    run_scrubber(server, manifest, dryrun=0)