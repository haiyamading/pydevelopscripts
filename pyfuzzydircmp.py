# -*- coding: utf-8; -*-
# pyfuzzydircmp.py compares all files in one directory with another 
# directory regardless of the subdirectory.
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
import subprocess
import sys
import getopt

import filecmp


compare = "C:\\Program Files (x86)\\Beyond Compare 3\\BCompare.exe"

def main(argv):                         
    right = None
    left  = None
    
    try:                                
        opts, args = getopt.getopt(argv, "hl:r:", ["help", "right", "left"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-r", "--right"):
            right = arg 
        elif opt in ("-l", "--left"):
            left = arg 
            
    if right == None and left == None:
        usage()
        exit(1)
        
    return fuzzyCompare( left, right )
    
    
def usage():
    print '-h,--help'
    print '-l,--left=Path for left'
    print '-r,--right=Path for right'

def getFiles( root ):
    map = {}
    
    for (dirpath, dirnames, filenames) in walk(root):
        for file in filenames :
            if not file.endswith( ".o" ):
                map[file] = path.join( dirpath, file )
            
    return map

    
def fuzzyCompare( left, right ):
    print
    print 'Comparing ...'
    print left, ' <=> ', right
    print
    map_left  = getFiles(left)
    map_right = getFiles(right)
    
    keys_left  = set( map_left.keys() )
    keys_right = set( map_right.keys() )
    
    print 'Intersection'
    keys = (keys_left & keys_right)

    for key in keys :
        print key
        print 'left:  ', map_left[key]
        print 'right: ', map_right[key]
        equal = filecmp.cmp( map_left[key], map_right[key] )
        print 'equal: ', equal
        print 
        if not equal :
            subprocess.call([compare, map_left[key], map_right[key]])

    
if __name__ == '__main__':
    main(sys.argv[1:])
 