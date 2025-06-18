"""shelves doc string"""

from __future__ import print_function

def validate_permission(
    protections_list,
    protection    
):
    if protection not in protections_list:
        print("protection {} does not exist in table\n".format(protection))
        return False
    return True

def find_permissions_by_depot(
    protections_list,
    depot
):
    results = [_ for _ in protections_list if '//{}/'.format(depot) in _['path']]
    return results


def find_permissions_by_stream(
    protections_list, 
    stream
):
    results = [_ for _ in protections_list if stream in _['path']]
    return results


def delete_permissions(
    server, 
    permissions_dict, 
    permissions
):

    print("Not Implemented")
    return


def get_protections_table(server):
    raw_protect_list = server.fetch_protect()["Protections"]
    perm_table_list = []

    for entry in raw_protect_list:
        comment = ""
        if "## " in entry:
            entry, comment = entry.split("## ")
        while "  " in entry:
            entry = entry.replace("  ", " ")

        entry_split = [_.replace("\n", "") for _ in entry.split(" ")]

        if len(entry_split) < 5:
            continue

        perm_table_list.append(
            {
                "access": entry_split[0],
                "type": entry_split[1],
                "name": entry_split[2],
                "host": entry_split[3],
                "path": entry_split[4],
                "comment": comment,
            }
        )

    return perm_table_list


def validate_protection(protection):
    if not {"access", "type", "name", "host", "path"}.issubset(set(protection.keys())):
        print(
            "Required protection field missing skipping entry: {}".format(
                protection.get("name", "Invalid")
            )
        )
        return False
    return True


def save_protections_table(protections_table, server, dryrun=0):
    protection_lines = []
    for entry in protections_table:
        entry_line = "{access} {type} {name} {host} {path}".format(
            access=entry["access"],
            type=entry["type"],
            name=entry["name"],
            host=entry["host"],
            path=entry["path"],
        )
        if entry["comment"]:
            entry_line = entry_line + " ## {}".format(entry["comment"])

        protection_lines.append(entry_line)

    if dryrun:
        print("=" * 40)
        print("Projected protection table edits:")
        print(protection_lines)
        print("=" * 40)
    else:
        result = server.save_protect({"Protections": protection_lines})
        print(result[0], "\n")