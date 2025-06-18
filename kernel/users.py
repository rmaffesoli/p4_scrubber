"""users doc string"""

from __future__ import print_function


def find_user_by_name(server, name
        
):
    # p4 user joe
    user_query = server.fetch_user(name)
    if not user_query.get("Update"):
        print("User {} does not exists\n".format(name))
        return
    print('Not implemented')
    return

def find_users_by_name(server, to_delete_list
        
):
    # p4 user joe
    print('Not implemented')
    return

def delete_user(server,
        
):
    # p4 user -D -F -y sammy
    print('Not implemented')
    return

def delete_users(server,
        
):
    # p4 user -D -F -y sammy
    print('Not implemented')
    return