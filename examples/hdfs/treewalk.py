# BEGIN_COPYRIGHT
# 
# Copyright 2009-2013 CRS4.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
# 
# END_COPYRIGHT

"""
Traverse an HDFS tree and output disk space usage by block size.
"""

import sys
import pydoop.hdfs as hdfs
from common import isdir, MB, TEST_ROOT


def treewalker(fs, root_info):
  yield root_info
  if root_info['kind'] == 'directory':
    for info in fs.list_directory(root_info['name']):
      for item in treewalker(fs, info):
        yield item


def usage_by_bs(fs, root):
  stats = {}
  root_info = fs.get_path_info(root)
  for info in treewalker(fs, root_info):
    if info['kind'] == 'directory':
      continue
    bs = int(info['block_size'])
    size = int(info['size'])
    stats[bs] = stats.get(bs, 0) + size
  return stats


def main():
  fs = hdfs.hdfs()
  try:
    root = "%s/%s" % (fs.working_directory(), TEST_ROOT)
    if not isdir(fs, root):
      sys.exit("%r does not exist" % root)
    print "BS(MB)\tBYTES"
    for k, v in usage_by_bs(fs, root).iteritems():
      print "%.1f\t%d" % (k/float(MB), v)  
  finally:
    fs.close()


if __name__ == "__main__":
  main()
