#!/usr/bin/python

# Script that generate an inclusions database from a config file and a base
# output directory.

import os
import sys

import inclusions_config
import inclusions_database


def generate_inclusions(chromium_root, config_filename, output_dir):
  config = inclusions_config.ReadConfigFromFile(config_filename, chromium_root)
  inclusions_db = inclusions_database.GenerateInclusionsDatabase(config)
  inclusions_database.WriteInclusionsDbToDisk(inclusions_db, output_dir)


if __name__ == '__main__':
  chromium_path = sys.argv[1]
  config_path = sys.argv[2]
  output_path = sys.argv[3]
  generate_inclusions(chromium_path, config_path, output_path)
