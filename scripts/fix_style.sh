#!/bin/bash

# Run the formatter in place.
yapf -r -i --style chromium .

# Run pylint over all python files.
# TODO: This doesn't print filename and line.
# How can I get it to do that?
for f in $(find . -iname "*.py")
do
  pylint $f
done
