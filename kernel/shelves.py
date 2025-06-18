"""shelves doc string"""

from __future__ import print_function


def validate_shelve(server, cl_number):
    shelved_client_results = server.run('changes', '-s', 'shelved')
    shelved_changelist_numbers = {_['change'] for _ in shelved_client_results}
    if cl_number not in shelved_changelist_numbers:
        print("Changelist {} does not contain shelfed files\n".format(cl_number))
        return False
    return True

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