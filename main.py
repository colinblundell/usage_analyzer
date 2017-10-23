#!/usr/bin/python

import argparse
import inclusions_analyzer
import getopt
import sys

from operator import itemgetter


def main(argv):
  inclusions_analyzer.analyze_inclusions()

  #signature = codesearch.getSignatureFor("src/components/signin/core/browser/signin_investigator.h", "GetAuthenticatedAccountId")
  #xrefs = codesearch.getXrefsFor(signature)
  #print xrefs
  #print
  #print callgraph


if __name__ == '__main__':
  main(sys.argv)
