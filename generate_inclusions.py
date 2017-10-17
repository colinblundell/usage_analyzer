#!/usr/bin/python

import pprint
import sys

import db
import inclusions_generator

if __name__ == '__main__':
  config_filename = sys.argv[1]
  output_filename = sys.argv[2]
  config = db.read_config_from_file(config_filename)

  generator = inclusions_generator.InclusionsGenerator(config)
  including_files_to_included_files = generator.map_including_files_to_included_files()
  included_files_to_including_files = generator.map_included_files_to_including_files()

  output_db = db.generate_output_database(config, 
                                          included_files_to_including_files, 
                                          including_files_to_included_files)
  printer = pprint.PrettyPrinter(indent=2)
  printer.pprint(output_db)
  #db.write_output_db_to_file(output_db, output_filename)
