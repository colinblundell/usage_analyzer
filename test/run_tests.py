#!/usr/bin/python

import os
import sys
import unittest

# Add the parent directory to the path.
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from test_inclusions_generator import *

if __name__ == '__main__':
  unittest.main()