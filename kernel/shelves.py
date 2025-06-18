"""shelves doc string"""

from __future__ import print_function


def find_shelves_by_user(
    server,
    user,
    dryrun=0
):
    shelved_client_results = server.run('changes', '-u', user, '-s', 'shelved')
    shelved_changelist_numbers = {_['change'] for _ in shelved_client_results}
    return shelved_changelist_numbers


def find_shelves_by_client(
    server, 
    client, 
    dryrun=0
):
    shelved_client_results = server.run('changes', '-c', client, '-s', 'shelved')
    shelved_changelist_numbers = {_['change'] for _ in shelved_client_results}
    return shelved_changelist_numbers


def delete_shelf(
    server, 
    client, 
    dryrun=0
):
    # p4 change -d 77
    print("Not Implemented")
    return