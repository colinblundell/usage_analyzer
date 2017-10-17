#!/usr/bin/python

import sys

import inclusions_config
import inclusions_database
import inclusions_generator

if __name__ == '__main__':
  config_filename = sys.argv[1]
  config = inclusions_config.read_config_from_file(config_filename)

  generator = inclusions_generator.InclusionsGenerator(config)
  output_db = generator.generate_inclusions_database()
  inclusions_database.write_output_db_to_disk(output_db)
