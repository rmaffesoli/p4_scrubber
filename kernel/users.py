"""users doc string"""

from __future__ import print_function

def validate_user(server, user_name):
    existing_user_names = {_['User'] for _ in server.iterate_users()}
    if user_name not in existing_user_names:
        print("User {} not found \n".format(user_name))
        return False
    return True

def delete_user(server, user, dryrun=0):
    if dryrun:
        result = "would have deleted user, {}".format(user) 
    else:
        result = server.run('user', '-D', '-F', '-y', user)
        if isinstance(result, list):
            result = result[0]
    
    return result
