#
#
# Read a fiber file and generate the corresponding sparse graph
#
#

import argparse
import sys
from fibergraph import FiberGraph
from fiber import FiberReader


#
# 
#
def main():

    parser = argparse.ArgumentParser(description='Read the contents of MRI Studio file and generate a sparse connectivity graph in SciDB.')
    parser.add_argument('--count', action="store", type=int, default=-1)
    parser.add_argument('file', action="store")
    parser.add_argument('output', action="store")

    result = parser.parse_args()
    reader = FiberReader(result.file)

    # Create the graph object
    # get dims from reader
    fbrgraph = FiberGraph ( reader.shape )

    # Open the output file
    try:
      fout = open ( result.output, 'w+' )
    except:
      print "Could not truncate or create file ", result.output
      sys.exit(-1)

    # Print the high-level fiber information
    print(reader)

    count = 0

    # iterate over all fibers
    for fiber in reader:
        count += 1
        # add the contribution of this fiber to the 
        fbrgraph.add(fiber)
        if result.count > 0 and count >= result.count:
            break
        if count % 1000 == 0:
          print ("Processed %d fibers", count )

    # output graph to SciDB ingest format
    fbrgraph.writeForSciDB( [65536,65536], fout )

    del reader

    return

if __name__ == "__main__":
      main()
