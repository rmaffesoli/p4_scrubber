"""users doc string"""

from __future__ import print_function

def validate_user(server, user_name):
    existing_user_names = {_['User'] for _ in server.iterate_users()}
    if user_name not in existing_user_names:
        print("User {} not found \n".format(user_name))
        return False
    return True

def delete_user(server, user, dryrun=0):
    # p4 user -D -F -y sammy
    if dryrun:
        result = "would have deleted user, {}".format(user) 
    else:
        result = server.run('user', '-D', '-F', '-y', user)
        if isinstance(result, list):
            result = result[0]
    
    print(result)
    return result

if __name__ == '__main__':
    from utils import setup_server_connection
    server = setup_server_connection(
        port="ssl:helix:1666", user="rmaffesoli"
    )
    user = 'delete_me_user'
    delete_user(server, user, dryrun=0)

