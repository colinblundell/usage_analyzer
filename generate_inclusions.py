#!/usr/bin/python

# Script that generate an inclusions database from a config file and a base
# output directory.

import os
import sys

import inclusions_config
import inclusions_database


def generate_inclusions(config_filename, output_dir):
  # TODO: Parameterize this.
  chromium_root = os.path.join(os.environ["HOME"], "chromium", "src")
  config = inclusions_config.ReadConfigFromFile(config_filename,
                                                   chromium_root)
  inclusions_db = inclusions_database.GenerateInclusionsDatabase(config)
  inclusions_database.WriteInclusionsDbToDisk(inclusions_db, output_dir)


if __name__ == '__main__':
  config_path = sys.argv[1]
  output_path = sys.argv[2]
  generate_inclusions(config_path, output_path)
