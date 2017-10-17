#!/usr/bin/python

import sys

import inclusions_config
import inclusions_database

if __name__ == '__main__':
  config_filename = sys.argv[1]
  config = inclusions_config.read_config_from_file(config_filename)

  inclusions_db = inclusions_database.generate_inclusions_database(config)
  inclusions_database.write_inclusions_db_to_disk(inclusions_db)
