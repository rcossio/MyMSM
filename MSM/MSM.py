import numpy as np
import sys
import argparse
import glob

# ------------------------------------------
#    Parse                
# ------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('-lt','--lag_time', dest="LagTime"    ,  required=True,  help="Lag time, multiple of sample time (integer)")
parser.add_argument('-o','--output',    dest="OutputFile",  required=True,   help="Output file with MSM eigenvectors")
parser.add_argument('-i','--input',     dest="InputWildcard",   required=True,   help="Wildcard to find the names of membership files file, e.g., mysequences*.dat")
parser.add_argument('-nv','--num_vec',  dest="NVectors", required=True,      help="Number of vectors to write in output file")
parser.add_argument('-s','--spectrum',  dest="SpectrumFile", required=True,  help="Eigenvalue spectrum file")


args = parser.parse_args()
LagTime  = int(args.LagTime)
NVectors = int(args.NVectors)
InputWildcard  = args.InputWildcard
OutputFile = args.OutputFile
SpectrumFile = args.SpectrumFile


#--------------------------------------------
#    Open InputFile reading the following 
#    format: 
#
#    #Coments...........
#         1    state
#         2    state
#         3    state
#    
#--------------------------------------------
InputFileList = glob.glob(InputWildcard)

print InputFileList
exit()
data=[]

for line in open(InputFile):

    # Skip comments (not you, the python script)
    if line.strip()[0] == "#" :
        continue

    # Define features array
    array = line.split()[1:]

    # Checks if length is the same  
    if len(data) == 0:
        length0 = len(array)

    length = len(array)
    if length != length0:
        sys.exit('tICA.py: Error. Some line of input file contains incomplete data.')


    # Add coordinates array to samples array
    data.append( array )

data = np.array(data,dtype=np.float64)


#-------------------------------------------
#    Compute transition matrix
#-------------------------------------------
sequences=[7,9,9,7,8,7]
sequences= np.asarray(sequences)
classes = np.unique(sequences)
n_states=3 
mapping = dict(zip(classes, range(n_states)))
mapping_fn = np.vectorize(mapping.get, otypes=[np.int])

