import os
import sys
from argparse import ArgumentParser

from PyQt6.QtWidgets import QApplication

from p4templates.ui.p4_template_loader_gui import P4TemplateLoaderDialog
from p4templates.kernel.utils import load_server_config, read_json

def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", default="./config.json")
    parser.add_argument("-m", "--manifest", default="./manifest.json")
    parsed_args = parser.parse_args()

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




if __name__ == "__main__":
    main()
