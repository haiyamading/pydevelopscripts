# -*- coding: utf-8; -*-
# pyfindduplicatefiles.py checks for files in a list of directories 
# and searches files with the same name.
#
# Copyright (C) 2015  monte <at> mibix.de
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from os import walk
from os import path
from collections import defaultdict

import subprocess
import sys
import getopt
import hashlib
import filecmp

verbose = 0

def main(argv):                         

    if( len(argv) < 1 ):
        usage()
        return

    return findDup( argv )
    
    
def usage():
    print('dir1 dir2 ... dirn')


def getFiles( root, map ):
    exclude_dir  = set([".git", ".metadata", "tmp", "objchk_win7_amd64", "objfre_win7_amd64", "objfre_wxp_x86", "objchk_wxp_x86"])
    #exclude_ext  = (".o", ".obj", ".exp", ".suo", ".gitmodules", ".user", ".xpj", ".pdb", ".idb", ".ilk", ".dep", ".log", ".mac", ".manifest", ".mark", ".tmh", ".xml", ".prefs", ".htm", ".bat", ".cmd", ".dll", ".sys", ".cat", ".inf", ".ico", "SOURCES", ".gitignore", "dirs", "dirs")
    include_ext   = (".c", ".h", ".cpp", ".s", ".C", ".H", ".CPP", ".S" )

    for (dirpath, dirnames, filenames) in walk(root, topdown=True):
        
        dirnames[:]  = [d for d in dirnames  if d not in exclude_dir]
        #filenames[:] = [f for f in filenames if not f.endswith( exclude_ext ) ]
        filenames[:] = [f for f in filenames if f.endswith( include_ext ) ]
        
        for file in filenames :
            map[file].add( path.join( dirpath, file ) )
            
    return map

def findDupPrintMap(map):
    for key, list in map.items():
        if verbose:
            print('-'*75)
            print( key )
            for path in list : print( path )
        elif len(list) > 1:
            print('-'*75)
            for path in list : print( path, "\t", md5(path))

def md5(fname):
    hash = hashlib.sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()[:8]
    
def findDup( folders ):
    print
    print('Searching ...', folders)
    print
    map = defaultdict(set)
    
    for folder in folders:
        getFiles(folder, map)
        
    findDupPrintMap(map)

    
if __name__ == '__main__':
    main(sys.argv[1:])
 