"""shelves doc string"""

from __future__ import print_function


def validate_group(server, group_name):
    existing_groups = {_['Group'] for _ in server.iterate_groups()}
    if group_name not in existing_groups:
        print("Group {} not found \n".format(group_name))
        return False
    return True


def delete_group(server, group, dryrun=0):
    # p4 group -d -F groupname
    if dryrun:
        result = "would have deleted group, {}".format(group) 
    else:
        result = server.run('group', '-d', '-F', group)
        if isinstance(result, list):
            result = result[0]
    
    print(result)
    return result


if __name__ == '__main__':
    from utils import setup_server_connection
    server = setup_server_connection(port="ssl:helix:1666", user="rmaffesoli")
    group = 'delete_me_group'
    delete_group(server, group, dryrun=0)