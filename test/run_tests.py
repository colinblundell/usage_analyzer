#!/usr/bin/python

import os
import sys
import unittest

# Add the parent directory to the path.
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# Import all tests to run.

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from test_common_utils import *
from test_including_to_included_analyzer import *
from test_inclusions_database import *
from test_inclusions_generator import *
from test_generate_inclusions import *

if __name__ == '__main__':
  unittest.main()
