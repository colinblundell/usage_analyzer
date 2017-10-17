#!/usr/bin/python

import sys

import db
import inclusions_generator

if __name__ == '__main__':
  config_filename = sys.argv[1]
  output_filename = sys.argv[2]
  config = db.read_config_from_file(config_filename)

  generator = inclusions_generator.InclusionsGenerator(config)
  output_db = generator.generate_inclusions_database()
  db.write_output_db_to_file(output_db, output_filename)
