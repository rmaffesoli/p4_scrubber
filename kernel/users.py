"""users doc string"""

from __future__ import print_function


def find_user_by_name(server, name
        
):
    user_query = server.fetch_user(name)
    if not user_query.get("Update"):
        print("User {} does not exists\n".format(name))
        return
    print('Not implemented')
    return

def find_users_by_name(server,
        
):
    print('Not implemented')
    return

def delete_user(server,
        
):
    print('Not implemented')
    return

def delete_users(server,
        
):
    print('Not implemented')
    return