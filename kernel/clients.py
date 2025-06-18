"""clients doc string"""

from __future__ import print_function


def find_clients_by_user(server, user, dryrun=0
        
):
    # p4 clients -u USER
    print('Not implemented')
    return


def find_clients_by_stream(server, stream):
    client_names = {_['client'] for _ in server.run('clients', '-S', stream)}
    return client_names


def delete_client(server, client, dryrun=0
        
):
    # p4 client -fd CLIENT
    print('Not implemented')
    return


def delete_clients(server, clients, dryrun=0
        
):
    # p4 client -fd CLIENT
    print('Not implemented')
    return