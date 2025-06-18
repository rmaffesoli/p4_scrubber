"""users doc string"""

from __future__ import print_function

def validate_user(server, user_name):
    existing_user_names = {_['User'] for _ in server.iterate_users()}
    print(existing_user_names)
    if user_name not in existing_user_names:
        print("User {} not found \n".format(user_name))
        return False
    return True

def delete_user(server, user, dryrun=0):
    # p4 user -D -F -y sammy
    print('Not implemented')
    return

def delete_users(server,users, dryrun=0):
    # p4 user -D -F -y sammy
    print('Not implemented')
    return