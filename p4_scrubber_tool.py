import os
import sys
from argparse import ArgumentParser


from p4_scrubber.kernel.utils import load_server_config, read_json, setup_server_connection, write_json
from p4_scrubber.kernel.scrubber import run_scrubber


def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", default="./config.json")
    parser.add_argument("-m", "--manifest", default="./manifest.json")
    parser.add_argument("-y", "--yes", default=0)
    parsed_args = parser.parse_args()

    dryrun=1
    if not parsed_args.yes:
        print('doing it live')
        dryrun=0

    script_dir = os.path.dirname(__file__)
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(script_dir)
    
    config_path = parsed_args.config
    config_path = os.path.abspath(config_path)

    manifest_path = parsed_args.manifest
    manifest_path = os.path.abspath(manifest_path)

    if not os.path.exists(config_path):
        print('A valid server configuration file is required')
        return
        
    if not os.path.exists(manifest_path):
        print('A valid manifest file is required')
        return


    config = load_server_config(config_path)
    manifest = read_json(manifest_path)
    p4_connection = setup_server_connection(**config['server'])
    
    updated_manifest = run_scrubber(p4_connection, manifest, dryrun)
    write_json(updated_manifest, manifest_path)





if __name__ == "__main__":
    main()
