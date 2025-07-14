"""clients doc string"""

from __future__ import print_function


def validate_client(server, client_name):
    existing_clients = {_['Client'] for _ in server.iterate_clients()}
    if client_name not in existing_clients:
        print("Client {} not found \n".format(client_name))
        return False
    return True

def find_clients_by_user(server, user):
    client_names = {_['client'] for _ in server.run('clients', '-u', user)}
    return client_names


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