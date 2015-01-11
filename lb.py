#!/usr/bin/env python3
#
# lb.py --- Little brother, a script for analysing who accesses your website
#
# Copyright (c) 2015 Bastian Rieck 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import collections
import ipaddress
import re
import sys

def readNetworks(filename):
  """
  Reads a list of networks from a file. The file should contain an IP address
  or an IP network with a bitmask, followed by a description. The description
  is to be separated from the IP network by at least one whitespace character.

  The function will ignore any lines that do not seem to contain an IP address
  or an IP network.
  """

  networks = list()

  with open(filename) as f:
    for line in f:
      matches = re.match(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,3})?)(?:\s+)(.*$)", line)
      if matches:
        address     = matches.group(1)
        description = matches.group(2)

        networks.append( (ipaddress.ip_network(address), description) )

  return networks

def readLog(filename):
  """
  Reads an Apache log. The file is supposed to contain an IP address as its
  first token. The function will only look for said IP address and count how
  often it occurs in the log file.
  """

  addresses = list()

  with open(filename) as f:
    for line in f:
      m = re.match(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
      if m:
        addresses.append( ipaddress.ip_address(m.group(1)) )

  return collections.Counter(addresses)

#
# main
#

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: lb.py NETWORKS LOG\n")
    sys.exit(-1)

  networks  = readNetworks(sys.argv[1])
  addresses = readLog(sys.argv[2])

  for address, count in addresses.most_common():
    for network, description in networks:
      if address in network:
        print("Counted %d visits from %s (%s)" % (count, address, description))
