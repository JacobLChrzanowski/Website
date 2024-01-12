#!/usr/bin/python3

import os
import click 
import Config.config_helper as conf
from Config.config import Config, Args_Obj
from Logging.logging_handler import setup_logging
import logging as log
DDNS_FOLDER = os.path.dirname(os.path.dirname(__file__))
ETC_FOLDER = os.path.join(DDNS_FOLDER, 'etc')
SITES_PATH = os.path.join(ETC_FOLDER, 'sites.yaml')

@click.command()
@click.option('--dryrun', '-n', is_flag=True, default=False)
@click.option('--verbose', '-v', is_flag=True, default=False)
@click.option('--debug', '-d', is_flag=True, default=False)
def main(dryrun: bool, verbose: bool, debug: bool):
    args = Args_Obj(dryrun, verbose, debug)
    setup_logging(verbose, debug, DDNS_FOLDER)
    conf.get_config(etc_folder=ETC_FOLDER,
                    yaml_path=SITES_PATH,
                    args=args)

    #TODO: print config
    for push in Config.pushes:
        push.update()

    log.info('Done')
    
    # exit()

if __name__ == '__main__':
    main()